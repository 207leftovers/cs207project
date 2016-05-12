import set_compiler
set_compiler.install()

import pyximport
pyximport.install()

import numpy as np

import KF

if __name__ == '__main__':

	sigeta = np.random.normal(0,1,2000)#scipy.stats.norm.rvs(0, 1, 2000)
	sigeps = np.random.normal(0,10,2000)#scipy.stats.norm.rvs(0, 10, 2000)

	mus = np.cumsum(sigeta)+20
	y = mus + sigeps

	thetas = []
	for i in np.arange(1, 21, 1):
	    for j in np.arange(1, 21, 1):
	        thetas += [KF.logL_LL(i,j, y)]

	print(thetas)