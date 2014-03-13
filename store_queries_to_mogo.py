# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:33:53 2013

@author: Javier Suarez
"""
from pymongo import MongoClient
import buildingTrainData as btd
import time


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
    

def storeAolSearch():
    """
    This function stores the AolSearch data set into MongoDB
    """
    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
    file_name = "rawQueries.txt"    
    db = dbClient()
    t0 = time.clock()
    for aol_line in open(path + file_name):
        iD,q,qt,r,url = aol_line.split('\t')        
        aol_query = {"anonID": str(iD), 
                     "query": str(q),
                	"queryTime": str(qt),
                     "itemRank": str(r),
                	"clickURL": str(url)    
        }
        #print aol_query
        #Inserting Documents (AOl_Queries)
        aol_search = db.aol_search
        query_id = aol_search.insert(aol_query)
        #print query_id
    
    print "Storing AolDataset into MongoDB: ", time.clock() - t0, "seconds."
    
def storeAolQuidder():
    """
    This function stores the AolSearch dataset into MongoDB 
    with another properties (pos and triGram).
    """
    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
    file_name = "rawQueries.txt"    
    db = dbClient()
    t0 = time.clock()
    for aol_line in open(path + file_name):
        iD,q,qt,r,url = aol_line.split('\t')        
        #Getting POS tags from Goal
        pos_vector = btd.posTagging(q)
        #Getting TriGrams from the POST obtained above.
        pos_string = ' '.join(pos_vector)
        pos_string = "S " + pos_string + " E"
        pos_string = pos_string.strip(' \t\r\n') 
        tgram = btd.nGram(3, pos_string)        
        query = {"anonID": str(iD), 
                 "query": str(q),
                	"queryTime": str(qt),
                 "itemRank": str(r),
                 	"clickURL": str(url), 
                 "pos" : pos_vector, 
                 "triGram" : tgram    
        }
        #Inserting Documents (AOl_Goals)
        aol_quidder = db.aol_quidder
        query_id = aol_quidder.insert(query)        
    
    print "Storing AolDataset into MongoDB: ", time.clock() - t0, "seconds."  

def storeAolGoals():
    """
    This function stores the AolSearch dataset into MongoDB 
    and other properties (pos and triGram).
    """
    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
    file_name = "aolGoals.txt"    
    db = dbClient()
    t0 = time.clock()
    for aol_line in open(path + file_name):
        q = aol_line.strip(' \t\r\n')
        #Getting POS tags from Goal
        pos_vector = btd.posTagging(q)
        #Getting TriGrams from the POST obtained above.
        pos_string = ' '.join(pos_vector)
        pos_string = "S " + pos_string + " E"
        pos_string = pos_string.strip(' \t\r\n') 
        tgram = btd.nGram(3, pos_string)
        aol_goal = {"query": str(q),
                    "pos" : pos_vector, 
                    "triGram" : tgram
        }
        #Inserting Documents (AOl_Goals)
        aol_goals = db.aol_goals
        query_id = aol_goals.insert(aol_goal)
        #print query_id
    
    print "Storing AolDataset into MongoDB: ", time.clock() - t0, "seconds."    
    
def addPosFieldIntoCollection():
    """
    This function insert a new property (POS - Part-of-speech) 
    in all documents from "test_sample" collection.
    """
    db = dbClient()
    #test_sample is just a proof. It will be change for a whole dataset
    pos_test = db.pos_test
    cursor = pos_test.find()
    for q in cursor:
        ID = q["_id"]        
        query = q["query"]
        pos = btd.posTagging(query)
        test_sample.update({'_id' : ID}, {'$set' : {'pos' : pos }})
    print "End"
    
def addNGramFieldIntoCollection():
    """
    This function insert a new property (triGram) obtained from POS tags
    in all documents from "test_sample" collection.
    """
    db = dbClient()
    #test_sample is just a proof. It will be change for a whole dataset
    ngram_test = db.ngram_test
    cursor = ngram_test.find()
    for q in cursor:
         ID = q["_id"]
         pos_vector = q["pos"]
         pos_string = ' '.join(pos_vector)
         pos_string = "S " + pos_string + " E"
         pos_string = pos_string.strip(' \t\r\n')                  
         tgram = btd.nGram(3, pos_string)
         ngram_test.update({'_id' : ID}, {'$set' : {'triGram' : tgram }})
    
       

def test():
    db = dbClient()
    aol_goals = db.aol_goals
    cursor = aol_goals.find()
    for q in cursor:
        tgram = q["triGram"]   
        print tgram
        for tg in tgram:
            print tg
            for t in tg:
                print t
        
    
    
    



