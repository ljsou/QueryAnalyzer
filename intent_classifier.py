# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 12:44:22 2014

@author: javier
"""

from textblob import TextBlob
from matplotlib import pyplot
import matplotlib as mpl
import nltk
#from textblob.taggers import NLTKTagger
from textblob.classifiers import NaiveBayesClassifier
import pickle


def extract_entities(text):
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):            
            if hasattr(chunk, 'node'):                               
                    print chunk.node + ': \t', ' '.join(c[0] for c in chunk.leaves())
                    """                
                if (chunk.node == 'PERSON'):
                    print "The query is: Informational"
                    
                elif (chunk.node == 'ORGANIZATION'):
                    print "The query is: Informational"
                    """                            

def generateClassifier():
    train = [("company", "navigational"), 
             ("business", "navigational"),
             ("organization", "navigational"),
             ("arrangement", "navigational"),
             ("administration", "navigational"),
             ("constitution", "navigational"),
             ("http", "navigational"),
             ("https", "navigational"),
             ("university", "navigational"),
             ("movies", "transactional"),
             ("song", "transactional"),
             ("lyrics", "transactional"),         
             ("images", "transactional"),
             ("humor", "transactional"),
             ("porn", "transactional"),         
             ("games", "transactional"),
             ("game", "transactional"),
             ("buy", "transactional"),
             ("jpeg", "transactional"),
             ("zip", "transactional"),
             ("install", "transactional"),       
             ("ways to", "informational"),
             ("hot to", "informational"),
             ("what is", "informational"),
             ("where is", "informational"),
             ("who", "informational"),
             ("where", "informational"),
             ("list", "informational"),
             ("playlist", "informational"),
             ("like this", "informational"),
             ("that", "informational"),
             ("this", "informational"),
             ("university", "informational"),
             ("country", "informational"),
             ("resources", "informational")
             ]

    cl = NaiveBayesClassifier(train)
    cl.show_informative_features(5)    
    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    saveTrainedClassifier(path, cl, "intent_classifier.pickle")
    
    
    
def classify(cl, query):
    #query = "download a song"
    prob_dist = cl.prob_classify(query)
    tag = cl.classify(query) 
    tns = prob_dist.prob("transactional")
    inf = prob_dist.prob("informational")
    nav = prob_dist.prob("navigational")
    print
    print "The query is: \t", tag
    print "Transactional: \t", tns
    print "Informational: \t", inf
    print "Navigational: \t", nav
    print
    return tag,tns, inf, nav
    
    
def viewProbabilityDistribution(tns, inf, nav):
                
    fig = pyplot.figure(figsize=(8,3))
    ax1 = fig.add_axes([0.09, 0.80, 0.82, 0.15])
    ax2 = fig.add_axes([0.05, 0.475, 0.9, 0.15])
    
    cmap = mpl.cm.cool
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    
    
    
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')
    space = "                                  "    
    cb1.set_label('Informational ' + space + ' Navigational' + space + ' Transactional')
    
    cmap = mpl.colors.ListedColormap(['#2EFEF7', '#0080FF', 'w', '#DF01D7'])
    cmap.set_over('0.25')
    cmap.set_under('0.75')
    informational = round(inf,2)
    navigacional = informational + round(nav,2)
    transactional = 1 - round(tns,2)
    
    bounds = [0, informational, navigacional, transactional, 1]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
                                         norm=norm,
                                         extend='both',
                                         ticks=bounds, # optional
                                         spacing='proportional',
                                         orientation='horizontal')
    

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
    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    f = open(path + classifier_name)
    loaded_cl = pickle.load(f)
    f.close()
    return loaded_cl