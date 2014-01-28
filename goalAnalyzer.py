# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 20:13:56 2013

@author: Javier Suarez

This script analyzes a user query through different levels of abstraction, 
ranging from natural language processing to identify the user's intentions 
and goals
"""

from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

import time
import buildingTrainData as bltd

import pickle


    
def accuracy(classifier):
    """
    This function evaluates the accuracy of the implemented classifier 
    Return the trained classifier 
    """
    t0 = time.clock()
    print "Loading Classifier, this may take several minutes, please wait..."
    cl = bltd.loadTrainedClassifier(classifier)
    print "Most predictive features: ", cl.show_informative_features(20)
    print  "\tClassifier loaded on", time.clock() - t0, "seconds."
    print 
    
    t0 = time.clock()
    print "Start data load, this may take several minutes, please wait..."
    db = bltd.dbClient()  
    aol_goals = db.aol_goals
    cursor = aol_goals.find({}, {"triGram" : 1}) 
    test_data = []
    t = ""
    label = "pos" 
    for td in cursor:
        tgram = td["triGram"]        
        #print tgram
        for tg in tgram:
            d = '-'.join(tg)
            t = t + " " + d
        test_data.append((t, label))
        t = ""
    print "Test data loaded on", time.clock() - t0, "seconds."   
    #print test_data  
    print 
    t0 = time.clock()
    print "Performing test, please wait..."
    print "Accuracy: ", cl.accuracy(test_data)    
    print    


def posTaggingDocument(sentence):
    """
    This function performs a Part-of-speech taggin per sentence (document).
    """
    t = TextBlob(sentence)
    p = ''
    for pt in t.tags:
        p+= str(pt[1]) + " "
    return p
    

def test(query, classifier):
    """
    This function classifies the user query as appropriate: "Pos" or "Neg".
    """
    p = posTaggingDocument(query)
    classifier.classify(p)
    prob_dist = classifier.prob_classify(p)
    #print "Max Probability Distribution:", prob_dist.max()
    #print "Pos:", prob_dist.prob("pos")
    #print "Neg:", prob_dist.prob("neg")
    return prob_dist.max(), prob_dist.prob("pos"), prob_dist.prob("neg")


def updateClassifier(query, classifier, label):
    """
    This feature allows updating the classifier based on new vocabulary (queries not seen in the training phase).
    """
    post = posTaggingDocument(query)
    new_data = [(post, label)]
    classifier.update(new_data)
    
    
def saveTrainedClassifier(path, classifier, classifier_name):
    f = open(classifier_name, 'wb')
    pickle.dump(classifier, f)
    f.close()
    

def loadTrainedClassifier(classifier_name):
    """
    This function allows to load a trained classifier.
    Return: loaded classifier
    """
    f = open(classifier_name)
    loaded_cl = pickle.load(f)
    f.close()
    return loaded_cl

#The following commands allow to observe the operation of this script.
"""    
>>> import goalAnalyzer as ga
>>> train, test = ga.init()
>>> train = ga.posTaggingCollection(train)
>>> test = ga.posTaggingCollection(test)
>>> cl = ga.accuracy(train, test)
>>> query = 'where to find info on aquarium in atlanta ga' #Example
>>> label = ga.test(query, cl)
>>> updateClassifier(query, cl, label)
>>> cl.accuracy(test)    
>>> 
>>>
>>> import pickle
>>> f = open('my_classifier.pickle', 'wb')
>>> pickle.dump(cl, f)
>>> f.close()
>>> 
>>>
>>> f = open('my_classifier.pickle')
>>> classifier = pickle.load(f)
>>> f.close()
""" 


    
