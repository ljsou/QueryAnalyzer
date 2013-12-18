# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 10:22:46 2013

@author: javier
"""

import goalAnalyzer as ga
import time

cl = ga.loadTrainedClassifier('my_classifier.pickle')
cl.show_informative_features(5)

path = '/media/University/UniversityDisc/2-Master/MasterThesis/EjecuciónTesis/Desarrollo/PythonProjects/Data/'
file_name = 'aolGoals.txt'

positives = []
negatives = []

print "plese wating..."
t0 = time.clock()
for line in open(path + file_name):    
    result = ga.test(line.strip(' \t\r\n'), cl)
    if result[0].strip(' \t\r\n') == 'pos':
        print "pos", line
        positives.append(line)
    else:
        print "neg", line
        negatives.append(line)

print "Test done", time.clock() - t0, "seconds."
print "Positives:", len(positives)
print "Negatives:", len(negatives)


    
    
    