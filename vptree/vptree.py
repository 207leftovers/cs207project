#Required for making unique id's and keeping track of nodes
import uuid
import numpy as np


class vpnode():
    def __init__(self):
        self.parent = None
        self.leftChild = None
        self.rightChild = None

    #Using preorder in a similar way as the lab
    #returns a list and not a generator object

    def preorder(self):
        if self.rightChild == None and self.leftChild == None:
            return [(self, None, None)]
        else:
            return [(self, self.leftChild, self.rightChild)] + self.leftChild.preorder() +\
                    self.rightChild.preorder()


#Since a VP tree has two kind of nodes - non-leaf nodes with vantage points and leaf nodes with closest possible candidates.

class vpnodeVP(vpnode):
    """
    Intermediate nodes with vantage points
    """
    def __init__(self, uid, pk, median, leftChild, rightChild):
        """
        pk - future input from timeseries
           - currently the id for the test timeseries
        """
        #Inheriting from the base class
        super().__init__()
        self.uid = uid
        self.pk = pk
        self.median = median
        self.leftChild = leftChild
        self.rightChild = rightChild


class vpnodeLeaf(vpnode):
    """
    Leaf nodes with primary key lists with the closest matches
    """
    def __init__(self, uid, pkList):
        super().__init__()
        self.uid = uid
        self.pkList = pkList


#Building the tree class
class vptree():
    """
    Main tree class
    """

    def __init__(self, allPk, vpList, dfunc):
        """
        allPK - List of all primary keys
        vpList - List of vantage points
        dfunc - distance function
        """
        self.vpList = vpList
        self.dfunc = dfunc
        self.root = self.maketree(allPk, vpList)

    
    def maketree(self, allPk, vpList):
        #Making an id for the node:
        uid = uuid.uuid1().int % 10000

        #checking if there are vantage points left
        #if we have none left, its just the vpnodeLeaf node
        if not vpList == []:
            return vpnodeLeaf(allPk, uid)

        else:
            #Decide how to pick vantage point
            #Currently using random selection
            index = np.random.choice(range(len(vpList)))
            VP = vpList[index]
            #Computing distance for all points
            VPdist = self.dfunc(VP, allPk)
            median = np.median(VPdist)

            #Assigning if left or right
            #initializing empty lists
            left_PK, left_VP, right_PK, right_VP = [], [], [], []
            for key, dist in zip(allPK, VPdist):
                if dist < median : #assigning left
                    left_PK.append(key)
                    if key in vpList and key != VP:
                        #add the key to vantage key list
                        left_VP.append(key)

                else:
                    right_PK.append(key)
                    if key in vpList and key != VP:
                        #add key to vantage key list
                        right_VP.append(key)

            leftChild = self.maketree(left_PK, left_VP)
            rightChild = self.maketree(right_PK, right_VP)

            #creating root node
            node = vpnodeVP(uid, VP, median, leftChild, rightChild)
            #setting parents
            rightChild.parent = node
            leftChild.parent = node
            return node
    


if __name__ == "__main__":
    data = np.random.rand(200) 
    dataDict = {}
    for i in range(len(data)):
        dataDict['key'+str(i+1)] = data[i]
    allPk = list(dataDict.keys())
    testvps = ['key7', 'key10', 'key45', 'key73']
    #creating distance function
    def absdist(VP,allPk):
        """
        Implementing basic absolute distance function
        """
        x = data[VP]
        y = np.array([data[key] for key in allPk])
        return np.abs(x-y)
    tree = vptree(allPk, testvps, absdist) 

