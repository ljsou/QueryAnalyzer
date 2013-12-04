# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:43:17 2013

@author: javier
"""

"""
This script allows to get all not empty queries from AOL dataset
"""

def writeFile(file_name, queryList):
    document = open(file_name, 'a')    
    for line in queryList:        
        document.write(line)
    document.close
    
def writeLineOn(file_name, line):
    document = open(file_name, 'a')    
    document.write(line)
    document.close

queries = []

print "Wait..."
path = "/home/javier/Desarrollo/PythonProject/"
for i in range(1, 2):
    collection = path + "user-ct-test-collection-" + str(i) + ".txt"
    print "user-ct-test-collection-" + str(i) + ".txt"
    for line in open(collection):
        iD,q,qt,r,url = line.split('\t')
        if((len(url) > 2) & (q != '-')):
            #print line.split('\t')
            queries.append(line)
            writeLineOn("rawQueries.txt", line)
    print "user-ct-test-collection-" + str(i) + " size:", len(queries)     

print "finish"
