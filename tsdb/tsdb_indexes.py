from collections import defaultdict
from operator import and_
from functools import reduce
import operator
import pickle
import os
import struct
import portalocker
from tsdb.tsdb_row import *

class ValueRef(object):
    " a reference to a string value on disk"
    def __init__(self, referent=None, address=0):
        self._referent = referent #value to store
        self._address = address #address to store at
        
    @property
    def address(self):
        return self._address
    
    def prepare_to_store(self, storage):
        pass

    @staticmethod
    def referent_to_bytes(referent):
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        return bytes.decode('utf-8')
    
    def get(self, storage):
        "read bytes for value from disk"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        "store bytes for value to disk"
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))
            
class BinaryNodeRef(ValueRef):
    "reference to a btree node on disk"
    
    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        "have a node store its refs"
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        "use pickle to convert node to bytes"
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        "unpickle bytes to get a node object"
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )

class BinaryNode(object):
    @classmethod
    def from_node(cls, node, **kwargs):
        "clone a node with some changes from another one"
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
        )

    def __init__(self, left_ref, key, value_ref, right_ref):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref

    def store_refs(self, storage):
        "method for a node to store all of its stuff"
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls
        #BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores
        #the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)

class Storage(object):
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        self._f = f
        self.locked = False
        #we ensure that we start in a sector boundary
        self._ensure_superblock()
    def _ensure_superblock(self):
        "Guarantee that the next write will start on a sector boundary"
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        "If not locked, lock the file for writing"
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        "Go to beginning of file which is on sec boundary"
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        "Write data to disk, returning the adress at which you wrote it"
        #first lock, get to end, get address to return, write size
        #write data, unlock <==WRONG, dont want to unlock here
        #your code here
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        self.lock()
        self._f.flush()
        #make sure you write root address at position 0
        self._seek_superblock()
        #write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def get_root_address(self):
        #read the first integer in the file
        #your code here
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        return self._f.closed
        
class BaseTree(object):
    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()
        
    def commit(self):
        "Changes are final only when committed"
        # Triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        # Make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)
        
    def _refresh_tree_ref(self):
        "Get reference to new tree if it has changed"
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())
        
    def _follow(self, ref):
        "Get a node from a reference"
        #calls BinaryNodeRef.get
        return ref.get(self._storage)
    
    def _find_max(self, node):
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node
        
class BinaryTree(BaseTree):
    "Immutable Binary Tree class. Constructs new tree on changes"
    
    def get_all_keys(self):
        keys = []
        
        if not self._storage.locked:
            self._refresh_tree_ref()
            
        nodes = [self._follow(self._tree_ref)]
        
        # Loop through all nodes
        while len(nodes) > 0:
            node = nodes.pop(0)
            if node is not None:
                nodes.append(self._follow(node.left_ref))
                nodes.append(self._follow(node.right_ref))
                keys.append(node.key)
        return keys
    
    def has_key(self, key):
        "Checks if the key is in the tree"
        #return key in self._keys
        try:
            self.get(key)
        except:
            return False
        return True
    
    def get_as_row(self, key):
        "Get the value for a key as a DBRow"
        return DBRow.row_from_string(self.get(key))
        
    def get(self, key):
        "Get the value for a key as a String"
        #your code here
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value):
        "Set a new value in the tree. Will cause a new tree"
        # Try to lock the tree. If we succeed make sure
        # we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        # Get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        # Insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)
        # Add key to the set
        #self._keys.add(key)
        
    def _insert(self, node, key, a_value_ref):
        "Insert a new node creating a new path from root"
        #create a tree if there was none so far
        new_node = node
        if node is None:
            # New node
            new_node = BinaryNode(
                BinaryNodeRef(), key, a_value_ref, BinaryNodeRef())
        elif key < node.key:
            "Key less than node.key"
            new_node = BinaryNode(
                self._insert(
                    self._follow(node.left_ref), key, a_value_ref), 
                node.key, node.value_ref, node.right_ref)
        elif key > node.key:
            "Key more than node.key"
            new_node = BinaryNode(
                node.left_ref, node.key, node.value_ref,
                self._insert(
                    self._follow(node.right_ref), key, a_value_ref))
        else: 
            # Update an existing node
            new_node = BinaryNode.from_node(node, value_ref=a_value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key):
        "Delete node with key, creating new tree and path"
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)
        # Remove the key from the dictionary of keys
        #self._keys.remove(key)
        
    def _delete(self, node, key):
        "Underlying delete implementation"
        if node is None:
            raise KeyError
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._delete(
                    self._follow(node.left_ref), key))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._delete(
                    self._follow(node.right_ref), key))
        else:
            left = self._follow(node.left_ref)
            right = self._follow(node.right_ref)
            if left and right:
                replacement = self._find_max(left)
                left_ref = self._delete(
                    self._follow(node.left_ref), replacement.key)
                new_node = BinaryNode(
                    left_ref,
                    replacement.key,
                    replacement.value_ref,
                    node.right_ref,
                )
            elif left:
                return node.left_ref
            else:
                return node.right_ref
        return BinaryNodeRef(referent=new_node)
    
class ArrayBinaryTree(BaseTree):
    "Immutable Array Binary Tree class. Constructs new tree on changes, multiple values per key"
    
    def __init__(self, storage, convert):
        self._storage = storage
        self._refresh_tree_ref()
        self._convert = convert
        
    def get_all_keys(self):
        keys = []
        
        # TODO!!!!
        if not self._storage.locked:
            self._refresh_tree_ref()
            
        nodes = [self._follow(self._tree_ref)]
        
        # Loop through all nodes
        while len(nodes) > 0:
            node = nodes.pop(0)
            if node is not None:
                nodes.append(self._follow(node.left_ref))
                nodes.append(self._follow(node.right_ref))
                keys.append(node.key)
        return keys
        
    def has_key(self, key):
        "Checks if the key is in the tree"
        #return key in self._keys
        try:
            self.get(key)
        except:
            return False
        return True
        
    def get(self, key):
        value_str = self._get(key)
        value_list = value_str.split(' ')
        value_arr = []
        for value in value_list:
            value_arr.append(value)
        return value_arr
        
    def _get(self, key):
        "Get value array for a key"
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        
        # TODO!!!!
        if not self._storage.locked:
            self._refresh_tree_ref()
            
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value):
        "Set a new value in the tree. Will cause a new tree"
        # Try to lock the tree. If we succeed make sure
        # we dont lose updates from any other process
        
        # TODO: PUT THESE BACK
        if self._storage.lock():
            self._refresh_tree_ref()

        # Get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(str(value))
        # Insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)
        
    def _insert(self, node, key, a_value_ref):
        "Insert a new node creating a new path from root"
        #create a tree if there was none so far
        new_node = node
        if node is None:
            # New node
            new_node = BinaryNode(
                BinaryNodeRef(), key, a_value_ref, BinaryNodeRef())
        elif key < node.key:
            "Key less than node.key"
            new_node = BinaryNode(
                self._insert(
                    self._follow(node.left_ref), key, a_value_ref), 
                node.key, node.value_ref, node.right_ref)
        elif key > node.key:
            "Key more than node.key"
            new_node = BinaryNode(
                node.left_ref, node.key, node.value_ref,
                self._insert(
                    self._follow(node.right_ref), key, a_value_ref))
        else: 
            # Update an existing node
            new_values = self._follow(a_value_ref).split(' ')
            existing_values = self._follow(node.value_ref).split(' ')
            existing_values.extend(new_values)
            a_value_ref = ValueRef(str.join(' ', existing_values))
            new_node = BinaryNode.from_node(node, value_ref=a_value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key, value):
        "Delete value from node with key, creating new tree and path"
        "If node has no more values, then delete the node"
        # TODO: !!!!
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key, str(value))
        
    def _delete(self, node, key, value):
        "Underlying delete implementation"
        if node is None:
            raise KeyError
        elif key < node.key:
            "Moving left"
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._delete(
                    self._follow(node.left_ref), key, value))
        elif key > node.key:
            "Moving right"
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._delete(
                    self._follow(node.right_ref), key, value))
        else:
            "Got the right node, now remove the value from it"
            values = self._follow(node.value_ref).split(' ')
            if (value is not None) and (value not in values):
                raise ValueError('Could not remove value ', value ,' from node with key', key)
            else:
                if value is not None:
                    values.remove(value)
                if len(values) > 0:
                    "We still have multiple values in this node, so restore it"
                    a_value_ref = ValueRef(str.join(' ', values))
                    new_node = BinaryNode.from_node(node, value_ref=a_value_ref)
                else:
                    "This node can be disposed of as it no longer is storing anything"
                    left = self._follow(node.left_ref)
                    right = self._follow(node.right_ref)
                    if left and right:
                        replacement = self._find_max(left)
                        #left_ref = self._delete(self._follow(node.left_ref), replacement.key)
                        left_ref = self._delete(self._follow(node.left_ref), replacement.key, None)
                        new_node = BinaryNode(
                            left_ref,
                            replacement.key,
                            replacement.value_ref,
                            node.right_ref,
                        )
                    elif left:
                        return node.left_ref
                    else:
                        return node.right_ref
        return BinaryNodeRef(referent=new_node)