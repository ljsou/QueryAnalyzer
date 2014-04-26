# -*- coding: utf-8 -*-
"""
Created on Sun April 13, 2014

@author: Javier Suarez

This script analyzes a user query through different levels of abstraction, 
ranging from natural language processing to identify the user's goals
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
import time

def analizer(query, num_topics, dictionary, corpus, alpha):

    #num_words = 4;        
    
    alpha=alpha
    #lda = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, update_every=1, chunksize=50, passes=1)
    lda_2 = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, alpha=alpha, update_every=1, chunksize=50, passes=1)
    #lda_goals = [lda[c] for c in corpus]
    #lda_goals_2 = [lda_2[c] for c in corpus]
    """
    plt.clf()
    plt.hist([[len(t) for t in lda_goals], [len(t) for t in lda_goals_2]], np.arange(40))
    plt.ylabel('Nr of Queries')
    plt.xlabel('Nr of Goals')
    plt.text(3, 50, r'default alpha')
    plt.text(25, 40, 'alpha='+str(alpha))
    plt.show()
    """
    #print "LDA GOALS' TOPICS:"
    #ldam.viewTopics(lda, num_topics, num_words)
    
    goals_distribution = ldam.perQueryGoalProportions(query, dictionary, lda_2)
    max_goal = ldam.viewPerQueryGoalProportions(goals_distribution)
    show_goal = lda_2.show_topic(max_goal)
    #print show_goal
    new_goal = []
    for goal in show_goal:
        weight = goal[0]
        tag = goal[1]
        new_goal.append((tag, weight))
        
    # Compute the position of the words.
    elements = wordcloud.fit_words(new_goal, width=100, height=100)
    image_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    # Draw the positioned words to a PNG file.    
    wordcloud.draw(elements, path.join(image_path + 'image.png'), width=100, height=100, scale=2)    
    lda_model = lda_2
    return image_path, lda_model
    
def draw_goal(lda_model, topic):
    other_goal = lda_model.show_topic(topic)
    new_goal = []
    image_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    
    for goal in other_goal: weight = goal[0];tag = goal[1];new_goal.append((tag, weight))
    
    elements = wordcloud.fit_words(new_goal, width=100, height=100)
    wordcloud.draw(elements, path.join(image_path + 'other_image.png'), width=100, height=100, scale=2)  
    
    
def goals(query, num_topics, alpha):
    #query = "i want to buy a car"
    t0 = time.clock()
    dictionary, corpus = genco.getCorpus(query)
    #print corpus    
    image_path, lda_model = analizer(query, num_topics, dictionary, corpus, alpha)
    print  "analysis completed in", time.clock() - t0, "seconds."
    return image_path, lda_model