# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 12:44:22 2014

@author: javier
"""

from textblob import TextBlob
from matplotlib import pyplot
import matplotlib as mpl
import nltk
from sklearn import cross_validation
#from textblob.taggers import NLTKTagger
from textblob.classifiers import NaiveBayesClassifier
import pickle
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


def extract_entities(text):
    nodes = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):            
            if hasattr(chunk, 'node'):  
                    nodes.append(chunk.node)                             
                    print chunk.node + ': \t', ' '.join(c[0] for c in chunk.leaves())
                    """                
                if (chunk.node == 'PERSON'):
                    print "The query is: Informational"
                    
                elif (chunk.node == 'ORGANIZATION'):
                    print "The query is: Informational"
                  """                            
                  
def getIntentDataset():
    train = [("company", "navigational"), 
             ("business", "navigational"),
             ("organization", "navigational"),
             ("arrangement", "navigational"),
             ("administration", "navigational"),             
             ("that", "informational"),
             ("this", "informational"),
             ("university", "informational"),
             ("country", "informational"),
             ("resources", "informational"),
            ('mansions', 'ambiguous'),
            ('stationery embellishments', 'navigational'),
            ('radio veracrz', 'navigational'),
            ('car trailer makers in michigan', 'informational'),
            ('restarant', 'ambiguous'),
            ('classy hairstyles', 'navigational'),
            ('sacramento bee', 'navigational'),
            ('paris food', 'navigational'),
            ('dictionary', 'ambiguous'),
            ('list of state names', 'informational'),
            ("kirsten dnst's hairstyles", 'informational'),
            ('home remedies for hair growth', 'informational'),
            ('careerbilders.com', 'navigational'),
            ('myspace layots', 'navigational'),
            ('names', 'ambiguous'),
            ("constitution", "navigational"),
             ("http", "navigational"),
             ("https", "navigational"),
             ("university", "navigational"),
             ("movies", "transactional"),
             ("song", "transactional"),
             ("lyrics", "transactional"),         
             ("images", "transactional"),
             ("humor", "transactional"),
            ('magnssen', 'ambiguous'),
            ('resort vacations to go', 'informational'),
            ('waterbry hospital', 'navigational'),
            ('free sond waves', 'transactional'),
            ('brbank condos for rent', 'transactional'),
            ('free mastrbation clips videos', 'informational'),
            ('pierpoint landing', 'navigational'),
            ('perforating tool', 'navigational'),
            ('consew sewing machines', 'informational'),
            ('yahoo mail', 'navigational'),
            ('diagnostic spinal facet arthrography', 'informational'),
            ('wellington high school 1993 class renion', 'informational'),
            ('ask', 'ambiguous'),
            ('kids party games', 'informational'),
            ('who invented moon pies', 'informational'),
            ('debt collection laws', 'informational'),
            ('california natral prodcts', 'informational'),
            ('microsoft powerpoint', 'navigational'),
            ('sparknotes', 'ambiguous'),
            ('workaholic hsbands and how to keep them home', 'informational'),
            ("game", "transactional"),
             ("buy", "transactional"),
             ("jpeg", "transactional"),
             ("zip", "transactional"),
             ("install", "transactional"),       
             ("ways to", "informational"),
             ("hot to", "informational"),
             ("what is", "informational"),
             ("where is", "informational"),  
             ('epic cams', 'navigational'),
            ('sigs', 'ambiguous'),
            ('womans road bike', 'informational'),
            ('harbor freight tools', 'informational'),
            ('citizenship in the nation worksheets', 'informational'),
            ('jews sck', 'navigational'),
            ('cable boxes', 'navigational'),
            ('lenore', 'ambiguous'),
            ('fairest flora bnda', 'informational'),
            ('what to do abot nosiy next door', 'informational'),
            ('yahoo.com', 'navigational'),
            ('dogpile', 'ambiguous'),
            ('david r. rbinow m.d.', 'transactional'),
            ('craigslist', 'ambiguous'),
            ('agentcafe.com', 'navigational'),
            ('jimmy carter erption of mt. st. helens', 'informational'),
            ('classic video game systems for sale', 'informational'),
            ('how to start a online shop', 'informational'),
            ('bank of america online banking', 'informational'),
            ('antiqe german silver prses', 'informational'),
            ('solar system for adolescence', 'informational'),
            ('jaipore brewster', 'navigational'),
            ('slam book', 'navigational'),
            ('sn dresses', 'navigational'),
            ('pictre of drosophila salivary glands', 'informational'),
            ('wasa homes', 'navigational'),
            ('nalgas calientes', 'navigational'),
            ('petroero', 'ambiguous'),
            ('recapitalization', 'ambiguous'),
            ('arizona elite basketball', 'informational'),
            ('www..davidgevans.com', 'navigational'),
            ('lenore', 'ambiguous'),
            ('sper nalgas', 'navigational'),
            ('emerald stdio in staten island ny', 'informational'),
            ('wooden doll crib', 'informational'),
            ('1974 gremlin x', 'informational'),
            ('radio veracrz', 'navigational'),
            ('orange conty ny events', 'informational'),
            ('leadbelly story on-dvd movie', 'transactional'),
            ('travelocity', 'ambiguous'),
            ('nivision.com', 'navigational'),
            ('maryland criminal records', 'informational'),
            ('naghty thoghts', 'navigational'),
            ('lray caverns', 'navigational'),
            ('africa kenya newspapers', 'informational'),
            ('koika', 'ambiguous'),
             ("porn", "transactional"),         
             ("games", "transactional"),
             ("who", "informational"),
             ("where", "informational"),
             ("list", "informational"),
             ("playlist", "informational"),
             ("like this", "informational"),
            ('pickens cont ga', 'informational'),
            ('50cent', 'ambiguous'),
            ('nhl', 'ambiguous'),
            ('earthlink.net', 'navigational'),
            ('renT prTval', 'navigational'),
            ('jimfeist', 'ambiguous'),
            ('yoth gitar dress shirt', 'informational'),
            ('snset shores rv park', 'informational'),
            ('three modes of decay for potassim-40', 'informational'),
            ('afs advanced financial services', 'informational'),
            ('how to by for less than a dollar wholesale', 'transactional'),
            ('diagnosis of spinal facet capslar laxity', 'informational'),
            ('myspace spport', 'navigational'),
            ('garland naaman forest baseball', 'informational'),
            ('www.wagerweb.com', 'navigational'),
            ('gibson stainless steele flatware', 'informational'),
            ('iwon', 'ambiguous'),
            ('pineapple greencheeks', 'navigational'),
            ('sacramento conty jail', 'informational')
             ]       
    data = []
    for d in train:
        #print d[0]
        #print d[1]
        data.append(({'feature': d[0]}, d[1]))
    
    print data
    return data

def generateClassifier():
    train = getIntentDataset()

    cl = NaiveBayesClassifier(train)
    cl.show_informative_features(5)    
    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    saveTrainedClassifier(path, cl, "intent_classifier_2.pickle")
    
    
def getTrainAndTestData():
    db = dbClient()    
    training = db.training
    train_set = training.find()   
    
    dev_test = db.dev_test
    dev_test_set = dev_test.find()
    
    test = db.test
    test_set = test.find()  
    
    return train_set, dev_test_set, test_set
    
    
def formatData(cursor):
    data = []
    t = ""
    for td in cursor:
        tgram = td["triGram"]
        label = td["label"] 
        #print tgram
        for tg in tgram:
            d = '-'.join(tg)
            t = t + " " + d
        #print t        
        data.append(({'trigram': t}, label))
        t = ""    
        
    print "Data:", len(data)
    return data
    

def performTrain(train, dev_test):        
    cl = nltk.NaiveBayesClassifier.train(train)
    accuracy = nltk.classify.util.accuracy(cl, dev_test)
    print 'Cccuracy=%-8s' % (accuracy)        
    cl.show_most_informative_features(5)
    return cl    
    
    
def performCrossValidation(data, k):
    cv = cross_validation.KFold(len(data),k=k)
    print "CV", cv
    accuracy = 0.0
    i = 0
    for traincv, testcv in cv:        
        cl = nltk.NaiveBayesClassifier.train(data[traincv[0]:traincv[len(traincv)-1]])
        accuracy_p = nltk.classify.util.accuracy(cl, data[testcv[0]:testcv[len(testcv)-1]])
        accuracy = accuracy + accuracy_p
        print 'Iteration:%-8s partial_accuracy=%-8s' % (i, accuracy_p)        
        i += 1
    print 'Accuracy total=%8s' % (accuracy / 10.0)
    return cl


def generateIntentionalityClassifier():
    db = dbClient()    
    training = db.training
    cursor = training.find()    
    
    #Reducir la cantidad de registros 
    crs = list(cursor)    
    random.shuffle(crs)
    # split into 90% training and 10% test sets
    p = int(len(crs) * .01)
    cr_test = crs[0:p]        
        
    print "Test", len(cr_test)    
    
    data = []
    t = ""
    for td in cr_test:
        tgram = td["triGram"]
        label = td["label"] 
        #print tgram
        for tg in tgram:
            d = '-'.join(tg)
            t = t + " " + d
        #print t
        data.append((t, label))
        t = ""
    #print data
    cl = NaiveBayesClassifier(data)
    cl.show_informative_features(30)    
    path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    saveTrainedClassifier(path, cl, "my_classifier_v6.pickle")
    return cl


def validacioGoals(cl):
    db = dbClient()    
    aol_goals = db.aol_goals
    cursor = aol_goals.find()             
        
    print "Size:", cursor.count()
    errors = []    
    t = ""
    cl = loadTrainedClassifier("my_classifier_v7.pickle")
    for td in cursor:
        tgram = td["triGram"]    
        #print tgram
        
        for tg in tgram:
            d = '-'.join(tg)
            t = t + " " + d                
            name = {'trigram':t}
            #print name
            guess = cl.classify(name)  
            if guess == "neg":
                errors.append( (guess, t) )
        t = ""
    num = len(errors)
    den = cursor.count()
    print "Num:", num
    print "Den:", den
    print "Acuracy:",  float(num) /  float(den)
    return errors


    
def classify(cl, query):
    #query = "download a song"
    prob_dist = cl.prob_classify(query)
    tag = cl.classify(query) 
    tns = prob_dist.prob("transactional")
    inf = prob_dist.prob("informational")
    nav = prob_dist.prob("navigational")
    amb = prob_dist.prob("ambiguous")
    
    print
    print "The query is: \t", tag
    print "Transactional: \t", tns
    print "Informational: \t", inf
    print "Navigational: \t", nav
    print "Ambiguous: \t", amb
    print
    return tag,tns, inf, nav, amb
    
    
def viewProbabilityDistribution(tns, inf, nav, amb):
                
    fig = pyplot.figure(figsize=(8,3))
    ax1 = fig.add_axes([0.09, 0.80, 0.82, 0.15])
    ax2 = fig.add_axes([0.05, 0.475, 0.9, 0.15])
    
    cmap = mpl.cm.cool
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    
    tns=0.30296413812
    inf=0.34457902786575
    nav=0.136609112019
    amb=0.21584772199524999
    
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')
    space = "                                  "    
    cb1.set_label('Informational ' + space + ' Navigational' + space + ' Transactional' + space + ' Ambiguous')
    
    cmap = mpl.colors.ListedColormap(['#2EFEF7', '#0080FF', '#AC58FA', 'w', '#DF01D7'])
    cmap.set_over('0.25')
    cmap.set_under('0.75')
    informational = round(inf,2) 
    navigacional = informational + round(nav,2)
    transactional = navigacional + round(tns,2)
    ambiguous = 1 - round(amb,2)

    print "tns=%s, inf=%s, nav=%s, am=%sb" % (transactional,informational,navigacional,ambiguous)    
    
    bounds = [0, informational, navigacional, transactional, ambiguous, 1]
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
    f = open(path + classifier_name, 'wb')
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