# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:18:43 2014

@author: javier
"""

import numpy as np
 
 
def kl(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions
 
    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
        
    """
    p = getDistribution(p)
    q = getDistribution(q)    
    
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
 
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))
    
def getDistribution(dist):
    distribution = [0] * 50
    #print buckets    
    total = 0
    for d in dist:
        total = total + d[1]        
        distribution[d[0]-1] = d[1]

    return distribution