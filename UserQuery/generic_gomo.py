# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 18:47:32 2014

@author: javier
"""

import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s, level=logging.INFO')
logger = logging.getLogger()
logger.disabled = False

from gensim import corpora, models
import generate_corpora as genco
import lsamodel as lsam
import ldamodel as ldam
from os import path
import wordcloud
import matplotlib.pyplot as plt
import numpy as np
import time
from pylab import *


def initCorpora(model_path):
    corpus = genco.MyCorpus()    
    corpus_name = "corpus.mm"
    corpora.MmCorpus.serialize(model_path + corpus_name, corpus)

def loadCorpusDictionary(model_path):
    dictionary_file = "goal_dictionary.dict"
    corpus_file = "corpus.mm"
    dictionary = corpora.Dictionary.load(model_path + dictionary_file)
    corpus = corpora.MmCorpus(model_path + corpus_file)    
    return corpus, dictionary
    

def initLSI(train, num_topics, model_path):             
    corpus, dictionary = loadCorpusDictionary(model_path)
    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
    corpus_tfidf = tfidf[corpus]    
    if(train == True):
        print "True"        
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics) # initialize an LSI transformation
        lsi.save(model_path + 'model.lsi') # same for tfidf, lda, ...        
    else:
        print "False"
        lsi = models.LsiModel.load(model_path + 'model.lsi')
    #corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    #num_words = 4
    #lsam.viewTopics(lsi, num_topics, num_words)
    
    return lsi, tfidf, dictionary, corpus

def initDefaultLDA(num_topics, model_path):      
    t0 = time.clock()
    corpus, dictionary = loadCorpusDictionary(model_path)
    lda_1 = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, update_every=1, chunksize=1000, passes=1)
    lda_1.save(model_path + 'model_1.lda')
    print  "LDA model ready, on", time.clock() - t0, "seconds."
    return lda_1

def initLDAwithAlpha(num_topics, alpha, model_path):    
    t0 = time.clock()    
    corpus, dictionary = loadCorpusDictionary(model_path)
    lda_2 = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, alpha=alpha, update_every=1, chunksize=1000, passes=1)
    lda_2.save(model_path + 'model_2.lda')
    print  "LDA model ready, on", time.clock() - t0, "seconds."
    return lda_2

def drawLdaDistributions(lda_1, lda_2, alpha, model_path):
    corpus, dictionary = loadCorpusDictionary(model_path)
    l_1 = [lda_1[c] for c in corpus]    
    l_2 = [lda_2[c] for c in corpus]    
    
    plt.clf()
    plt.hist([[len(t) for t in l_1], [len(t) for t in l_2]], np.arange(60))
    plt.ylabel('Nr of Queries')
    plt.xlabel('Nr of Goals')
    plt.text(6, 15000, r'default alpha')
    plt.text(35, 25000, 'alpha='+str(alpha))
    plt.show()
            
    #print "LDA GOALS' TOPICS:"
    #ldam.viewTopics(lda, num_topics, num_words)    
    #ldaGoalDistribution(query, dictionary, lda_1, model_path)
    #ldaGoalDistribution(query, dictionary, lda_2, model_path)

def ldaGoalDistribution(goals_distribution, max_goal, image_path, lda_n, name):    
    show_goal = lda_n.show_topic(max_goal)
    print show_goal
    new_goal = []
    for goal in show_goal:
        weight = goal[0]
        tag = goal[1]
        new_goal.append((tag, weight))
        
    # Compute the position of the words.
    elements = wordcloud.fit_words(new_goal, width=100, height=100)
    
    # Draw the positioned words to a PNG file.    
    wordcloud.draw(elements, path.join(image_path + name), width=100, height=100, scale=2)                
    
def drawTags(model, lsi, query, dictionary, image_path, tfidf):
    print "Init drawTags"   
    goals_distribution = model.perQueryGoalProportions(query, dictionary, tfidf, lsi)
    max_goal = model.viewPerQueryGoalProportions(goals_distribution)    
    show_goal = lsi.show_topic(max_goal)
    print show_goal
      
    new_goal = []
    for goal in show_goal:
        weight = goal[0]
        tag = goal[1]
        new_goal.append((tag, weight))
        
    # Compute the position of the words.
    elements = wordcloud.fit_words(new_goal, width=100, height=100)    
    # Draw the positioned words to a PNG file.    
    wordcloud.draw(elements, path.join(image_path + 'lsa-image.png'), width=100, height=100, scale=2)    
    
    
def LSI(dictionary, tfidf, lsi, query, model_path):           
    drawTags(lsam, lsi, query, dictionary, model_path, tfidf)
    #return image_path
    
def draw_goal(lsi, topic):
    other_goal = lsi.show_topic(topic)
    new_goal = []
    image_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    
    for goal in other_goal: weight = goal[0];tag = goal[1];new_goal.append((tag, weight))
    
    elements = wordcloud.fit_words(new_goal, width=100, height=100)
    wordcloud.draw(elements, path.join(image_path + 'other_image.png'), width=100, height=100, scale=2)  