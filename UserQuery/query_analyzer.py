# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 20:13:56 2013

@author: Javier Suarez

This script analyzes a user query through different levels of abstraction, 
ranging from natural language processing to identify the user's intentions 
and goals
"""

import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s, level=logging.INFO')
logger = logging.getLogger()
logger.disabled = False

from gensim import models
import generate_corpora as genco
import ldamodel as ldam
import matplotlib.pyplot as plt
import numpy as np
from os import path
import wordcloud
from IPython.core.display import Image 

def estimator_intentions_goals(query, num_topics, dictionary, corpus):

    num_topics = 10;
    num_words = 4;        
    
    alpha=0.3
    lda = models.ldamodel.LdaModel(corpus, num_topics=25, id2word=dictionary, update_every=1, chunksize=50, passes=1)
    lda_2 = models.ldamodel.LdaModel(corpus, num_topics=25, id2word=dictionary, alpha=alpha, update_every=1, chunksize=50, passes=1)
    lda_goals = [lda[c] for c in corpus]
    lda_goals_2 = [lda_2[c] for c in corpus]
    
    plt.clf()
    plt.hist([[len(t) for t in lda_goals], [len(t) for t in lda_goals_2]], np.arange(40))
    plt.ylabel('Nr of Queries')
    plt.xlabel('Nr of Goals')
    plt.text(3, 150, r'default alpha')
    plt.text(25, 300, 'alpha='+str(alpha))
    plt.show()
    
    print "LDA GOALS' TOPICS:"
    ldam.viewTopics(lda, num_topics, num_words)
    
    goals_distribution = ldam.perQueryGoalProportions(query, dictionary, lda)
    max_goal = ldam.viewPerQueryGoalProportions(goals_distribution)
    
    show_goal = lda.show_topic(max_goal)
    #print show_goal
    new_goal = []
    for goal in show_goal:
        weight = goal[0]
        tag = goal[1]
        new_goal.append((tag, weight))
        
    # Compute the position of the words.
    elements = wordcloud.fit_words(new_goal, width=100, height=100)
    p = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    # Draw the positioned words to a PNG file.    
    wordcloud.draw(elements, path.join(p + 'image.png'), width=100, height=100, scale=3)    
    return p
    
def createCourpus(query, num_topics):
    #query = "i want to buy a car"
    dictionary, corpus = genco.getCorpus2(query)
    print corpus    
    p = estimator_intentions_goals(query, num_topics, dictionary, corpus)
    return p