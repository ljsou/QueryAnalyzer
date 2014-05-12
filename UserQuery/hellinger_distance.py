# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:17:23 2014

@author: javier

Three ways of computing the Hellinger distance between two discrete
probability distributions using NumPy and SciPy.
"""
 
import numpy as np
from scipy.linalg import norm
from scipy.spatial.distance import euclidean
 
 
_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64
 
 
def hellinger1(p, q, n):
    p = getDistribution(p, n)
    q = getDistribution(q, n)
    return norm(np.sqrt(p) - np.sqrt(q)) / _SQRT2
 
 
def hellinger2(p, q, n):
    p = getDistribution(p, n)
    q = getDistribution(q, n)
    return euclidean(np.sqrt(p), np.sqrt(q)) / _SQRT2
 
 
def hellinger3(p, q, n):
    p = getDistribution(p, n)
    q = getDistribution(q, n)
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2
    
def getDistribution(dist, n):
    #print dist
    distribution = [0] * n
    #print buckets    
    #total = 0    
    for d in dist:
        #total = total + d[1]        
        m = d[0]
        #print m
        distribution[m] = d[1]    
    return distribution
        