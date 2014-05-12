# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:00:00 2013

@author: Javier Suarez
"""

"""
List of Part-of-Speech tags of Penn Treebank Project
<http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html>

VB    Verb, base form
VBD    Verb, past tense
VBG    Verb, gerund or present participle
VBN    Verb, past participle
VBP    Verb, non-3rd person singular present
VBZ    Verb, 3rd person singular present
WRB    Wh-adverb
"""

import time
from pymongo import MongoClient
import random


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


def filterDataset(file_name, new_file):
    """
    This function allows to remove repeated lines from a dataset. 
    @file_name: dataset name to be filtered.
    @new_file: resulting dataset.
    """
    size = len(open(file_name).readlines())
    print size
    document = open(new_file, 'a')      
    #dataset = []        
    l = ''
    for line in open(file_name):
        if (line.strip(' \t\r\n') != l):
            #dataset.append(line.strip(' \t\r\n'))
            document.write(line.strip(' \t\r\n') + "\n")
            l = line.strip(' \t\r\n')  
    #print len(open(new_file).readlines())            
    document.close     
   

def filterDatasetByVerb(file_name, new_file, tag):
    """
    This function allows to remove queries with POS tags like VB, VBD, VBG, VBN, VBP and VBZ or WRB
    requires just adding a representative letter as: V or W.
    @file_name: dataset name to be filtered.
    @new_file: resulting dataset.
    @tag: a representative letter as: V or W.
    """
    t0 = time.clock()
    size = len(open(file_name).readlines())
    print size

    document = open(new_file, 'a')      
    
    for line in open(file_name):
        l = line.strip(' \t\r\n')        
        #if (l.find('V') == -1):  #Filter by Verb
        if (l.find(tag) == -1):   #Filter by Wh-words 
            #print l
            document.write(l + "\n")    
            
    document.close     
    print "Filter by verbs done on", time.clock() - t0, "seconds."
            

def randomSample(file_name, new_file, sample):
    """
    This function allow to take a random sample of a given dataset.
    @file_name: dataset name to be filtered.
    @new_file: resulting dataset.
    @sample: is the number with which the cycle should be increased at each iteration
    """
    t0 = time.clock()
    size = len(open(file_name).readlines())
    collection = []
    
    for line in open(file_name):
        collection.append(line.strip(' \t\r\n'))
    
    document = open(new_file, 'a')
    for i in range(0, size, sample):        
        print collection[i]
        document.write(collection[i] + "\n")
    document.close 
    print "Random sample from", file_name, "done on", time.clock() - t0, "seconds."


def insertIntoMongo(cursor, db):     
     for g in cursor:        
        query = g["query"]   
        post = g["post"]   
        triGram = g["triGram"]     
        label = g["label"]       
        data = {"query": query,
                 "post" : post, 
                 "triGram" : triGram, 
                 "label" : label
                 }

        training_dataset = db.training_dataset
        training_dataset.insert(data)


def createDataSetForTraining():
    """ 
    """
    db = dbClient()
    t0 = time.clock()  
    #test_sample is just a proof. It will be change for a whole dataset
    positive_training_sample_2 = db.positive_training_sample_2    
    cursor_ps = positive_training_sample_2.find()
    insertIntoMongo(cursor_ps, db)
    
    negative_training_sample_2 = db.negative_training_sample_2 
    cursor_ng = negative_training_sample_2.find()
    insertIntoMongo(cursor_ng, db)

    print "Test sample done on", time.clock() - t0, "seconds."



def subdivideTrainingDataset():
    """ 
    """
    t0 = time.clock()
    db = dbClient()
    #test_sample is just a proof. It will be change for a whole dataset
    training_dataset = db.training_dataset
    #aol_quidder = db.aol_quidder
    cursor = training_dataset.find()
    
    # shuffle corpus
    crs = list(cursor)    
    random.shuffle(crs)
    # split into 90% training and 10% test sets

    p = int(len(crs) * .9)
    cr = crs[0:p]
    q = int(len(cr) * .9)
    cr_train = cr[0:q]
    cr_dev_test = cr[q:]    
    cr_test = crs[p:]
    
    print "Train", len(cr_train)
    print "Test", len(cr_test)
    print "Dev test", len(cr_dev_test)
    
    
    for g in cr_train:        
        query = g["query"]   
        post = g["post"]   
        triGram = g["triGram"]           
        label = g["label"]    
        data = {"query": query,
                 "post" : post, 
                 "triGram" : triGram, 
                 "label" : label
        }        
        #Inserting Documents (training data)
        training = db.training
        training.insert(data)
    
    print "Training sample done on", time.clock() - t0, "seconds."
    t0 = time.clock()
    
    for g in cr_dev_test:        
        query = g["query"]   
        post = g["post"]   
        triGram = g["triGram"]  
        label = g["label"]          
        data = {"query": query,
                 "post" : post, 
                 "triGram" : triGram, 
                 "label" : label
        }
        #Inserting Documents (training data)
        dev_test = db.dev_test
        dev_test.insert(data)
    
    print "Dev test sample done on", time.clock() - t0, "seconds."
    t0 = time.clock()
                            
    for g in cr_test:        
        query = g["query"]   
        post = g["post"]   
        triGram = g["triGram"]   
        label = g["label"]         
        data = {"query": query,
                 "post" : post, 
                 "triGram" : triGram, 
                 "label" : label
        }
        #Inserting Documents (training data)
        test = db.test
        test.insert(data)
    
    print "Test sample done on", time.clock() - t0, "seconds."


def trainingPositiveSample():
    """
    This function allow to take a random sample of a given dataset in MongoDB.  
    In turn, the sample obtained from the original dataset is stored in MongoDB. 
    - For the positive_training_sample collection is necessary to use 
      the $in operator over aol_goals collection.
    - For the negative_training_sample collection is necessary to use 
      the $nin operator over aol_quidder collection.
    """
    t0 = time.clock()
    db = dbClient()
    #test_sample is just a proof. It will be change for a whole dataset
    aol_goals = db.aol_goals    
    cursor = aol_goals.find({"pos" : {"$in":["VB", "VBG", "WRB", "WP"]}})

    print "Train", cursor.count()
        
    #collection = []
    for g in cursor:        
        query = g["query"]   
        post = g["pos"]   
        triGram = g["triGram"]           
        data = {"query": query,
                 "post" : post, 
                 "triGram" : triGram, 
                 "label" : "pos"
        }

        #Inserting Documents (positive training data)
        positive_training_sample_2 = db.positive_training_sample_2
        positive_training_sample_2.insert(data)
        
    print "Random sample done on", time.clock() - t0, "seconds."


def trainingNegativeSample():
    """
    This function allow to take a random sample of a given dataset in MongoDB.  
    In turn, the sample obtained from the original dataset is stored in MongoDB. 
    - For the negative_training_sample collection is necessary to use 
      the $nin operator over aol_quidder collection.
    """
    t0 = time.clock()
    db = dbClient()
    i = 0   
    aol_quidder = db.aol_quidder
    cursor = aol_quidder.find({"pos" : {"$nin":["VB", "VBG", "WRB", "WP"]}})

    print "Train", cursor.count()
    
    for g in cursor:        
        query = g["query"]   
        pos = g["pos"]   
        triGram = g["triGram"]           
        data = {"query": query,
                 "post" : pos, 
                 "triGram" : triGram, 
                 "label" : "neg"
        }
        i += 1
        if(i == 184):
            i = 0
            negative_training_sample_2 = db.negative_training_sample_2
            negative_training_sample_2.insert(data)            
    
    print "Random sample done on", time.clock() - t0, "seconds."
        
        
def insertPerplexity(assessment):
    t0 = time.clock()
    db = dbClient()
    for a in range(len(assessment)):   
    
       alpha = assessment['A'][a]   
       topics = assessment['B'][a]  
       perplex = assessment['C'][a] 
       per_word_perplexity = assessment['D'][a] 
       elapsed_time = assessment['E'][a]       
       
       values = {"alpha": alpha,
                 "topics" : topics, 
                 "perplex" : perplex, 
                 "per_word_perplexity" : per_word_perplexity, 
                 "elapsed_time" : elapsed_time
       }   
       #Inserting Documents (AOl_Goals)
       lda_assessment = db.lda_assessment
       lda_assessment.insert(values)
       #negative_training_sample = db.negative_training_sample
       #negative_training_sample.insert(goal)       
     
    print "lda_assessment done on", time.clock() - t0, "seconds."
    
    
    
    
    
    
    
    
    
    
