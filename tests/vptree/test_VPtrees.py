from vptree import *
import numpy as np

data = np.random.rand(200) 
dataDict = {}
for i in range(len(data)):
    dataDict['key'+str(i+1)] = data[i]
allPk = list(dataDict.keys())
testvps = ['key7', 'key10', 'key45', 'key73']

# Creating distance function
def absdist(VP,allPk):
    """
    Implementing basic absolute distance function
    """
    x = dataDict[VP]
    y = np.array([dataDict[key] for key in allPk])
    return np.abs(x-y)

tree = VPtree(allPk, testvps, absdist)
vpt = tree.gen_graph()

def dist(vp,arg):
    x = dataDict[vp]
    return np.abs(x-arg)

search_val = np.random.normal(0,5)
allDists = np.array([np.abs(search_val - dataDict[p]) for p in allPk])
subset = tree.gen_subset(search_val,dist)
closest = min(allPk, key = lambda k:allDists[allPk.index(k)])
    
assert closest in subset