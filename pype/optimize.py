from .fgir import *
from .error import *

# Optimization pass interfaces

class Optimization(object):
  def visit(self, obj): pass

class FlowgraphOptimization(Optimization):
  '''Called on each flowgraph in a FGIR.
  May modify the flowgraph by adding or removing nodes (return a new Flowgraph).
  If you modify nodes, make sure inputs, outputs, and variables are all updated.
  May NOT add or remove flowgraphs.'''
  pass

class TopologicalFlowgraphOptimization(Optimization):
  '''Called on each flowgraph in a FGIR, in dependent order.
  Components which are used by other components will be called first.'''
  pass

class NodeOptimization(Optimization):
  '''Called on each node in a FGIR.
  May modify the node (return a new Node object, and it will be assigned).
  May NOT remove or add nodes (use a component pass).'''
  pass

class TopologicalNodeOptimization(NodeOptimization): pass

# Optimization pass implementations

class PrintIR(TopologicalNodeOptimization):
  'A simple "optimization" pass which can be used to debug topological sorting'
  def visit(self, node):
    print(str(node))

class AssignmentEllision(FlowgraphOptimization):
  '''Eliminates all assignment nodes.
  Assignment nodes are useful for the programmer to reuse the output of an
  expression multiple times, and the lowering transformation generates explicit
  flowgraph nodes for these expressions. However, they are not necessary for
  execution, as they simply forward their value. This removes them and connects
  their pre- and post-dependencies.'''

  def visit(self, flowgraph):
    # Check all the nodes in the flowgraph and remove assigment nodes
    to_remove = []
    
    # Keeps track of the predecessors to nodes to be removed
    to_remove_inputs = {}
    
    # Find all assignment nodes to remove
    for node in flowgraph.nodes.keys():
        # If the node is an assigment, eliminate it
        if flowgraph.nodes[node].type == FGNodeType.assignment:
            to_remove.append(node)
            to_remove_inputs[node] = flowgraph.nodes[node].inputs
    
    # Update the nodes that are before and after the assignment nodes
    for node in flowgraph.nodes.keys():
        for to_remove_node in to_remove_inputs:
            if to_remove_node in flowgraph.nodes[node].inputs:
                flowgraph.nodes[node].inputs.remove(to_remove_node)
                flowgraph.nodes[node].inputs.extend(to_remove_inputs[to_remove_node])
    
    for var in flowgraph.variables:
        node = flowgraph.variables[var]
        if node in to_remove:
            flowgraph.variables[var] = to_remove_inputs[node][0]
    
    # Clear out the nodes that should be removed
    for node_to_remove in to_remove:
        del flowgraph.nodes[node_to_remove]
    
    return flowgraph

class DeadCodeElimination(FlowgraphOptimization):
  '''Eliminates unreachable expression statements.
  Statements which never affect any output are effectively useless, and we call
  these "dead code" blocks. This optimization removes any expressions which can
  be shown not to affect the output.
  NOTE: input statements *cannot* safely be removed, since doing so would change
  the call signature of the component. For example, it might seem that the input
  x could be removed:
    { component1 (input x y) (output y) }
  but imagine this component1 was in a file alongside this one:
    { component2 (input a b) (:= c (component a b)) (output c) }
  By removing x from component1, it could no longer accept two arguments. So in
  this instance, component1 will end up unmodified after DCE.'''

  def visit(self, flowgraph):
    # Check all the nodes in the flowgraph and remove dead nodes
    # Start with assuming all nodes should be removed, and then 
    # work backwards from the outputs to remove unused ones
    to_remove = list(flowgraph.nodes.keys())
    # Need to copy this list, otherwise you are modifying the originals
    to_check = flowgraph.outputs[:]
    
    while len(to_check) > 0:
        cur = to_check.pop()
        to_remove.remove(cur)
        
        # Add all previous to the to_check queue
        for key in flowgraph.nodes[cur].inputs:
            if key in to_remove and key not in to_check:
                to_check.append(key)
    
    # Now eliminate whatever is left and hasn't been visited
    if len(to_remove) > 0:
        print("Removing nodes", to_remove)
    for key in to_remove:
        del flowgraph.nodes[key]
    
    to_remove_vars = []
    
    # Remove unused variables as well
    for var in flowgraph.variables:
        node = flowgraph.variables[var]
        if node in to_remove:
            to_remove_vars.append(var)
    for var in to_remove_vars:
        del flowgraph.variables[var]
        
    return flowgraph

class InlineComponents(TopologicalFlowgraphOptimization):
  '''Replaces every component invocation with a copy of that component's flowgraph.
  Topological order guarantees that we inline components before they are invoked.'''
  def __init__(self):
    self.component_cache = {}

  def visit(self, flowgraph):
    for (cnode_id, cnode) in [(nid,n) for (nid,n) in flowgraph.nodes.items() if n.type==FGNodeType.component]:
      target = self.component_cache[cnode.ref]
      # Add a copy of every node in target flowgraph
      id_map = {} # maps node id's in the target to node id's in our flowgraph
      for tnode in target.nodes.values():
        if tnode.type==FGNodeType.input or tnode.type==FGNodeType.output:
          newtype = FGNodeType.forward
        else:
          newtype = tnode.type
        n = flowgraph.new_node(newtype, ref=tnode.ref)
        id_map[tnode.nodeid] = n.nodeid
      # Connect all copies together
      for tid,tnode in target.nodes.items():
        flowgraph.nodes[id_map[tid]].inputs = [id_map[i] for i in tnode.inputs]
      # Link inputs of cnode to inputs of target flowgraph
      for cnode_input,targ_input in zip(cnode.inputs, target.inputs):
        flowgraph.nodes[id_map[targ_input]].inputs = [cnode_input]
      # Link output of target flowgraph to outputs of cnode
      for oid,onode in flowgraph.nodes.items():
        if cnode_id in onode.inputs:
          onode.inputs[onode.inputs.index(cnode_id)] = id_map[target.outputs[0]]
      # Remove all other references to cnode in flowgraph
      del flowgraph.nodes[cnode_id]
      victims = [s for s,nid in flowgraph.variables.items() if nid==cnode_id]
      for v in victims:
        del flowgraph.variables[v]
    self.component_cache[flowgraph.name] = flowgraph
    return flowgraph