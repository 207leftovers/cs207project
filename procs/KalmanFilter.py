# import sys
# sys.path.append('../')

import timeseries as ts
import numpy as np
import scipy.optimize

import asyncio

import set_compiler
set_compiler.install()

import pyximport
pyximport.install()

import filtering


def proc_main(pk, row, arg):

	ts1 = np.array(row['ts'].values())
	logL_LLy = lambda x: filtering.logL_LL(x[0], x[1], ts1)
	sigma_epsilon, sigma_eta = scipy.optimize.fmin(logL_LLy,[ts1.std()/2,ts1.std()/2])
	return [abs(sigma_epsilon), abs(sigma_eta)]

async def main(pk, row, arg):
    return proc_main(pk, row, arg)
