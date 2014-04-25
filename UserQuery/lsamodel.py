# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:02:13 2014

@author: javier
"""
#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#logger = logging.getLogger()
#logger.disabled = True

from gensim import corpora, models
from itertools import chain
import time
from pylab import *
import matplotlib.pyplot as plt
import numpy as np

path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
dictionary_name = 'goal_sample_dictionary.dict'
corpus_name = 'corpus.mm'

def initLSA (path, dictionary_name, corpus_name, ntopics):
    dictionary = corpora.Dictionary.load(path + dictionary_name)
    corpus = corpora.MmCorpus(path + corpus_name)
    #print corpus
    #print dictionary.token2id    

    tfidf = models.TfidfModel(corpus)   
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=ntopics)    
    topics = lsi.show_topics(num_topics=10, num_words=3, log=False, formatted=False)
    i = 0
    for tp in topics:
        print "TOPIC #", i, ": ", tp
        i=i+1
        
    lsi_corpus = lsi[corpus_tfidf]    

    return lsi, lsi_corpus, tfidf, dictionary
    
def viewTopics(model, num_topics, num_words):
    topics = model.show_topics(num_topics=num_topics, num_words=num_words, log=False, formatted=False)
    i = 0
    for tp in topics:
        print "TOPIC #", i, ": ", tp
        i=i+1
    

def viewThreshold(model_corpus):
    print model_corpus
    scores = list(chain(*[[score for topic,score in topic] \
                          for topic in [doc for doc in model_corpus]]))            
                          
    threshold = sum(scores)/len(scores)
    print "threshold", threshold
    return threshold    


def viewPerCorpusTopicDistribution(path, model_corpus):
    file_name = "aolGoalsSample.txt" 
    documents = open(path + file_name)    
    for i,j in zip(model_corpus,documents):
        print i, " ", j.strip(' \t\r\n')


def perQueryGoalProportions(query, dictionary, tfidf, lsa):
    t0 = time.clock()
    #print dictionary.token2id
    vec_bow = dictionary.doc2bow(query.lower().split())
    print "vec_bow: \t",  vec_bow
    vec_tfidf = tfidf[vec_bow] # convert the query to LSI space
    print "vec_tfidf:\t", vec_tfidf
    print    
    print "Per-query goal proportions (on", time.clock() - t0, "seconds):" 
    goal_proportion = lsa[vec_tfidf]
    print "\t", goal_proportion
    print 
    print
    return goal_proportion
    
def viewPerQueryGoalProportions(goals_distribution):
    proportion = []
    goals = []
    maximo = 0
    max_goal = 0
    for g in goals_distribution:
        proportion.append(abs(g[1]))
        goals.append(g[0])
        if abs(g[1]) > maximo:
            maximo = abs(g[1])
            #print g[1]
            max_goal = g[0]
       
        
    print "MAX:", max_goal
        
    #print proportion
    #print goals

    width = 0.5 # gives histogram aspect to the bar diagram
    pos = np.arange(len(goals))

    ax = plt.axes()
    ax.set_xticks(pos + (width / 2))
    ax.set_xticklabels(goals)
    
    plt.bar(pos, proportion, width, color='r')
    plt.ylabel('Goals distribution for query')
    plt.xlabel('Goals')
    plt.show()
    print
    print
    return max_goal
    

    


