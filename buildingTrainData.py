# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:10:12 2013

@author: Javier Suarez
"""
from textblob import TextBlob
from textblob.taggers import NLTKTagger
import time
from pymongo import MongoClient
import json 


def dbClient():
    """
    This function makes a Connection with MongoClient, i.e., 
    creates a MongoClient to the running mongod instance. 
    """
    #Making a Connection with MongoClient
    client = MongoClient('localhost', 27017)
    #Getting a Database
    db = client['aolSearchDB']
    return db
    
def createTrainingData():
    db = dbClient()    
    negative_training_sample = db.negative_training_sample
    cursor = negative_training_sample.find()
    for td in cursor:
        tgram = td["triGram"]
        label = td["label"]
        #train.append((tgram, label))
        training = {"text" : tgram, 
                 "label" : label                
                 }
        #Inserting Documents (AOl_Queries)
        training_data = db.train_data
        training_data.insert(training, safe = True)
    
def trainingData():
    data = ""
    db = dbClient()          
    training_data = db.training_data
    cursor = training_data.find({}, { "_id": 0, "label": 1 , "text": 1 }).limit(10)
    for td in cursor:
        data = data + json.dumps(td, sort_keys=True, indent=4, separators=(',', ': ')) + ", \n"
        
    data = "[" + data + "]"
    print data
    
    document = open("training.json", 'a')   
    document.write(data)
    document.close  
        
        

def addSomeLabel(path, file_name, label):
    """
    This function allows to add a tag in order to labeling a training set.
    Return tagged data set for training process
    """
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
    

def posTagging(phrase):
    #nltk_tagger = NLTKTagger()
    #t = TextBlob(phrase, pos_tagger=nltk_tagger)
    t = TextBlob(phrase)
    postg = t.tags 
    p = []
    for pt in postg:
        p.append(str(pt[1]).strip(' \t\r\n'))
    return p
    

def posTaggingFromDocument(train, file_name):
    """
    This function performs a POS tag process 
    @train: training file 
    @file_name: document name in which the pos tags are recorded
    """
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
    

def nGram(n, phrase):
    t = TextBlob(phrase)
    return t.ngrams(n=n)
    

def renderTrainData(path, positives, negatives):
    """
    render train data (Positives + Negavites)
    """
    pos = []
    neg = []
    
    pos = addSomeLabel(path, positives, 'pos')
    neg = addSomeLabel(path, negatives, 'neg')
    
    return pos + neg
        
    
    
    
    