# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:15:08 2013

@author: javier
"""

"""
This script allows to obtain a random set of POS Tags of explicit user goals 
"""

from textblob.classifiers import NaiveBayesClassifier   


def addPositiveLabelToPosTags():
    path = "/home/javier/Desarrollo/PythonProject/"
    goals = "trainPosTags.txt"
    
    train = []
    random_train = []
    
    for line in open(path + goals):
        query = line.strip(' \t\r\n')
        train.append(query)
    
    for line in range(0, 98294, 100):    
        #print line
        tag = "pos"
        data = []
        data.append(train[line])
        data.append(tag)
        random_train.append(tuple(data))
    
    print len(random_train)

#This function gets only Queries from rawQueires dataset (AOL)
def getRawQueires():        
    path = "/home/javier/Desarrollo/PythonProject/"
    queries = "rawQueries.txt"    
    document = open('queries.txt', 'a') 
    print "Wait..."
    for line in open(path + queries):
        q = line.split('\t')
        document.write(q[1].strip(' \t\r\n') + "\n")
    document.close
    print "Finished!"
    
def countLines(file_name):
    lines = len(open(file_name).readlines())
    print lines
    
    
        
    