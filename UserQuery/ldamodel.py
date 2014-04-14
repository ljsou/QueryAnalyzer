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
import re
import nltk


model_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
data_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
dictionary_name = 'goal_dictionary.dict'
corpus_name = 'corpus.mm'

def stop_words_set():
    stopwords = set(nltk.corpus.stopwords.words('english'))
    stopwords.remove("do")
    stopwords.remove('from')
    stopwords.remove('being')
    stopwords.remove('had')
    stopwords.remove('having')
    stopwords.remove('have')
    stopwords.remove('is')
    stopwords.remove('can')
    stopwords.remove('own')
    stopwords.remove('be')
    stopwords.remove('are')
    stopwords.remove('doing')
    stopwords.update(['aol', 'up', 'free', 'writes', 'money', 'baby', 'address', 'rid', 'music', 'space', 'name', 'pimp', 'account', 'http', 'assist', 'home', 'online', 'https', 'porn', 'sex', 'phone', 'myspace', 'password', 'people'])
    return stopwords

def initLDA (model_path, dictionary_name, corpus_name, ntopics):
    dictionary = corpora.Dictionary.load(model_path + dictionary_name)
    corpus = corpora.MmCorpus(model_path + corpus_name)
    #print corpus
    #print dictionary.token2id    

    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=ntopics, update_every=1, chunksize=1000, passes=1)
    lda.save(model_path + 'model.lda') # same for tfidf, lsi, ...  
    topics = lda.show_topics(topics=10, topn=3, log=False, formatted=False)
    i = 0
    for tp in topics:
        print "TOPIC #", i, ": ", tp
        i=i+1
            
    return lda, dictionary
    
def viewTopics(model, topics, topn):
    topics = model.show_topics(topics, topn, log=False, formatted=False)
    i = 0
    for tp in topics:
        print "GOAL #", i, ": ", tp
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


def perQueryGoalProportions(query, dictionary, lda):
    t0 = time.clock()
    #print dictionary.token2id
    vec_bow = dictionary.doc2bow(query.lower().split())
    #print "vec_bow: \t",  vec_bow    
    #print    
    print "Per-query goal proportions (on", time.clock() - t0, "seconds):" 
    goal_proportion = lda[vec_bow]
    #print goal_proportion
    print 
    print
    return goal_proportion

def perQueryGoalProportions_2(query, dictionary, lda):    
    temp = query.lower()
    punctuation_string = ['.',',',';','?','!','"']
    for i in range(len(punctuation_string)):
        temp = temp.replace(punctuation_string[i], '')

    words = re.findall(r'\w+', temp, flags = re.UNICODE | re.LOCALE)

    important_words = []
    important_words = filter(lambda x: x not in stop_words_set(), words)

    #dictionary = corpora.Dictionary.load('questions.dict')

    ques_vec = []
    ques_vec = dictionary.doc2bow(important_words)

    topic_vec = []
    topic_vec = lda[ques_vec]
    
    print topic_vec

    word_count_array = np.empty((len(topic_vec), 2), dtype = np.object)
    for i in range(len(topic_vec)):
        word_count_array[i, 0] = topic_vec[i][0]
        word_count_array[i, 1] = topic_vec[i][1]
        
        idx = np.argsort(word_count_array[:, 1])
        idx = idx[::-1]
        word_count_array = word_count_array[idx]
        
        final = []
        final = lda.print_topic(word_count_array[0, 0], 1)
        print final
        
        question_topic = final.split('*') ## as format is like "probability * topic"
        print question_topic
        
        print question_topic[1]

        
        
def viewPerQueryGoalProportions(goals_distribution):
    proportion = []
    goals = []
    maximo = 0
    max_goal = 0
    for g in goals_distribution:
        proportion.append(abs(g[1]))
        goals.append(g[0])
        #print g[1]
        if abs(g[1]) > maximo:
            maximo = abs(g[1])
            #print g[1]
            max_goal = g[0]
       
        
    print "MAX ", max_goal

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
    

    


