# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:10:12 2013

@author: Javier Suarez
"""
from textblob import TextBlob
#from textblob.taggers import NLTKTagger
from textblob.classifiers import NaiveBayesClassifier
from pymongo import MongoClient
import pickle
import json 
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
    
    
def createTrainingData():
    db = dbClient()    
    positive_training_sample = db.positive_training_sample
    cursor = positive_training_sample.find()
    data = []
    t = ""
    for td in cursor:
        tgram = td["triGram"]
        label = td["label"] 
        #print tgram
        for tg in tgram:
            d = '-'.join(tg)
            t = t + " " + d
        print t
        data.append((t, label))
        t = ""
        
    negative_training_sample = db.negative_training_sample
    cursor = negative_training_sample.find().limit(100)
    t = ""
    for td in cursor:
        tgram = td["triGram"]
        label = td["label"] 
        #print tgram
        for tg in tgram:
            d = '-'.join(tg)
            t = t + " " + d
        print t
        data.append((t, label))
        t = ""
    
    #print data
    print len(data)
    
    cl = NaiveBayesClassifier(data)
    cl.show_informative_features(20)    
    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer"
    saveTrainedClassifier(path, cl, "my_classifier_v3.pickle")

        
        #train.append((tgram, label))
        #training = {"text" : tgram, 
        #         "label" : label                
        #         }
        #Inserting Documents (AOl_Queries)
        #training_data = db.train_data
        #training_data.insert(training, safe = True)
    
def trainingData():
    """
    This function allows to obtain a JSON file from a collection in MongoDB.
    """
    data = ""
    db = dbClient()          
    training_data = db.training_data
    cursor = training_data.find({}, { "_id": 0, "label": 1 , "text": 1 })
    for td in cursor:
        data = data + json.dumps(td, sort_keys=True, indent=4, separators=(',', ': ')) + ", \n"
        
    data = "[" + data + "]"
    print data
    
    document = open("training.json", 'a')   
    document.write(data)
    document.close  
    

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
    """
    This function perform a n-gram process
    """
    t = TextBlob(phrase)
    return t.ngrams(n=n)


def saveTrainedClassifier(path, classifier, classifier_name):
    """
    This function allows to save the trained classifier like a file.pickle
    """
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
    
    
def test(classifier, query):
    q = posTagging(query)
    q = " ".join(q)
    print "POS Tags: ", q       
    tgram = nGram(3, q)  
    t = ""
    for tg in tgram:
        d = '-'.join(tg)
        t = t + " " + d
    
    print "TriGram: ", t
    
    prob_dist = classifier.prob_classify(t)
    print "Max Probability Distribution:", prob_dist.max()
    print "Pos:", prob_dist.prob("pos")
    print "Neg:", prob_dist.prob("neg")
    
    
    
    