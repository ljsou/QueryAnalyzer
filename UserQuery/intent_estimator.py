# -*- coding: utf-8 -*-
"""
Created on Sun April 13, 2014

@author: Javier Suarez

This script analyzes a user query through different levels of abstraction, 
ranging from natural language processing to identify the user's intents
"""

import intent_classifier as iclass    
import goal_analyzer as ga    
import time

    
def intent(query):
    t0 = time.clock()

    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    classifier_name = "my_classifier_v3.pickle"
    
    cl = ga.loadTrainedClassifier(path + classifier_name)
    prob_dist_max, tag = ga.testQuery(cl, query)    

    cl = iclass.loadTrainedClassifier("intent_classifier.pickle")
    tag,tns,inf,nav = iclass.classify(cl, query)
    
    ga.viewProbabilityDistribution(prob_dist_max, tag)    
    iclass.viewProbabilityDistribution(tns,inf,nav)    

    print  "analysis completed in", time.clock() - t0, "seconds."
    
    
