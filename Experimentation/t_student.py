# -*- coding: utf-8 -*-
"""
Created on Sat May 10 17:00:00 2014

@author: javier
"""

from scipy import stats
import numpy as np

def describe_sample(sample, name):
    n, (smin, smax), sm, sv, ss, sk = stats.describe(sample)
    print 'Distribution for %s'% name
    sstr = 'mean = %6.4f, variance = %6.4f, skew = %6.4f, kurtosis = %6.4f'
    print sstr %(sm, sv, ss ,sk)
    

def unpaired_ttest(significance_level, sample_a, sample_b):    
    describe_sample(sample_a, "Sample A: ")
    describe_sample(sample_b, "Sample B: ")    
    
    two_sample = stats.ttest_ind(sample_a, sample_b)
    if (two_sample[1] > significance_level):
        print "For Two-tailed hypothesis, the t-statistic is %.6f and the p-value is %.6f." % two_sample
        print "Therefore: the result is NOT significant at p < %s" % significance_level
    else:
        print "For Two-tailed hypothesis, the t-statistic is %.6f and the p-value is %.6f." % two_sample
        print "Therefore: the result is significant at p < %s" % significance_level
    # assuming unequal population variances
    #two_sample_diff_var = stats.ttest_ind(sample_a, sample_b, False)
    #print "If we assume unequal variances than the t-statistic is %.5f and the p-value is %.5f." % two_sample_diff_var
    print

def paired_ttest(significance_level, baseline, follow_up):
    paired_sample = stats.ttest_rel(baseline, follow_up)
    print "The t-statistic is %.6f and the p-value is %.6f." % paired_sample
    if (paired_sample[1] > significance_level):
        print "For Two-tailed hypothesis, the t-statistic is %.6f and the p-value is %.6f." % paired_sample
        print "Therefore: the result is NOT significant at p < %s" % significance_level
    else:
        print "For Two-tailed hypothesis, the t-statistic is %.6f and the p-value is %.6f." % paired_sample
        print "Therefore: the result is significant at p < %s" % significance_level
    print
    

def l_sample_ttest(x,n):
    #Descriptive Statistics
    #x = stats.t.rvs(10, size=1000)
    #x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,21,22,23,24,25,26,27]
    x = np.array(x)
    
    print "Para X"
    print x.max(), x.min()  # equivalent to np.max(x), np.min(x)
    print x.mean(), x.var() # equivalent to np.mean(x), np.var(x)
    print 
    
    m, v, s, k = stats.t.stats(10, moments='mvsk')
    n, (smin, smax), sm, sv, ss, sk = stats.describe(x)
    
    print 'distribution:',
    sstr = 'mean = %6.4f, variance = %6.4f, skew = %6.4f, kurtosis = %6.4f'
    print sstr %(m, v, s ,k)    
    
    print 'distribution for X:',
    sstr = 'mean = %6.4f, variance = %6.4f, skew = %6.4f, kurtosis = %6.4f'
    print sstr %(sm, sv, ss ,sk)
    
    print 'X:   t-statistic = %6.3f pvalue = %6.4f' %  stats.ttest_1samp(x, m)
    
    tt = (sm-m)/np.sqrt(sv/float(n))  # t-statistic for mean
    pval = stats.t.sf(np.abs(tt), n-1)*2  # two-sided pvalue = Prob(abs(t)>tt)
    print 't-statistic = %6.3f pvalue = %6.4f' % (tt, pval)

def confidence_interval(s):
    from scipy import stats
    import scipy as sp
    import numpy as np
    import math
    
    s = np.array(s)
    n, min_max, mean, var, skew, kurt = stats.describe(s)
    std=math.sqrt(var)
    
    
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.mlab as mlab
    
    sigma = np.sqrt(var)
    #x = np.linspace(-3,3,100)
    plt.plot(s,mlab.normpdf(s,mean,sigma))
    
    plt.show()    
    
    #note these are sample standard deviations 
    #and sample variance values
    #to get population values s.std() and s.var() will work
     
     
    #The location (loc) keyword specifies the mean.
    #The scale (scale) keyword specifies the standard deviation.
     
    # We will assume a normal distribution
    R = stats.norm.interval(0.05,loc=mean,scale=std)
    print R
    R = stats.norm.interval(0.95,loc=mean,scale=std/math.sqrt(len(s)))
    print R
    R = stats.t.interval(0.95,len(s)-1,loc=mean,scale=std/math.sqrt(len(s)))
    print R