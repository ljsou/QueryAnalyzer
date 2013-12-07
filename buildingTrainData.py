# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:10:12 2013

@author: Javier Suarez
"""
from textblob import TextBlob
import time

#path = "/home/javier/Desarrollo/PythonProject/Data/"
#goals = "aolGoals.txt"

#Allows to add tag in order to labeling a training set
def addSomeLabel(path, file_name, label):
    t0 = time.clock()
    train = []
    print "Add '", label,"' label to", file_name, "please wait..."
    for line in open(path + file_name):
        query = line.strip(' \t\r\n')
        tag = label
        data = []
        data.append(query)
        data.append(tag)
        train.append(tuple(data))
    #print train[:10]
    print "Labeled done on", time.clock() - t0, "seconds."
    return train


def posTagging(train, file_name):
    t0 = time.clock()
    print "Performing POS Tagging, please wait..."
    document = open(file_name, 'a')   
    for tr in train:
        #print tr.strip(' \t\r\n')
        t = TextBlob(tr.strip(' \t\r\n'))    
        postg = t.tags    
        p = ''
        #print postg
        for pt in postg:
            p = p + str(pt[1]) + " "
        #print p
        document.write(p + "\n")
    document.close    
    print "POS Taggin done on", time.clock() - t0, "seconds."


def renderTrainData(path, positives, negatives):
    pos = []
    neg = []
    
    pos = addSomeLabel(path, positives, 'pos')
    neg = addSomeLabel(path, negatives, 'neg')
    
    return pos + neg
    
    
