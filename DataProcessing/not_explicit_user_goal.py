# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:02:46 2013

@author: javier
"""

path = "/home/javier/Desarrollo/PythonProject/"
goals = "aolGoals.txt"
queries = "rawQueries.txt"

notExplicitUserGoals = []
intoDataset =[]

for line in open(path + goals):
    print line.strip(' \t\r\n')
    l = line.strip(' \t\r\n')
    for query in open(path + queries):
        q = query.strip(' \t\r\n')
        if(l == q):    
            print "TRUEEEEE"
            break
    
print "finished"
        
            