# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 20:13:56 2013

@author: javier
"""

from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

def init():
    train = [
         ('how to warm up your fish tank water.', 'pos'),
         ('how to freeze corn on cob', 'pos'),
         ('ways to delay your period or have it before the week its supposed to come', 'pos'),
         ('how to start computer in safe mode.', 'pos'),
         ("how to make your infant smart", 'pos'),
         ('making pumbaa costume.', 'pos'),
         ('find area code', 'pos'),     
         ('make your own skin bleaching cream','pos'),     
         ("how to treat african american hair", 'pos'),
         ('starting an independant record label', 'pos'),
         ('how to stop wood floors from squeaking.', 'pos'),
         ("make money now", 'pos'),
         ('learn to speak russian cleveland', 'pos'),
         ('find liences plate information', 'pos'),
         ('how to do knuckle push ups', 'pos'),
         ('how to whistle with your fingers', 'pos'),
         ('buying used cars online', 'pos'),
         ('feeding the labs', 'pos'),
         ('tipping out other employees', 'pos'),
         ('getting your own webpage for small businesses','pos'),
         ('where to buy placido tequila', 'pos'),
         ('westchester.gov', 'neg'),
         ('vera.org', 'neg'),
         ('ameriprise.com', 'neg'),
         ('ask.com', 'neg'),
         ('hepatitis b vaccine safety infants', 'neg'),
         ('yahoo.com', 'neg'),
         ('baby names', 'neg'),
         ('intel celeron m processor', 'neg'),
         ('www.samsclubguesspass.com', 'neg'),
         ('black gospel artists', 'neg'),
         ('rocky mountain news', 'neg'),
         ('microsoft', 'neg'),
         ('www.ballys casino atlantic city', 'neg'),
         ('xxx', 'neg'),
         ('aol cards.com', 'neg'),
         ('reggaeton videos', 'neg'),
         ('italian recipes','neg'),
         ('hotmail.com','neg'),     
         ('olympus digital 595 zoom instruction book','neg'),
         ('University of Cauca','neg'),
         ('all toxin shampoo','neg'),
         ('hot nude russian women','neg'),
         ('zero turn mowers','neg'),
         ('the jews are guilty','neg'),
         ('department of revenue services','neg'),
         ('walt disney world','neg'),
         ('free software', 'neg')
    ]
         
    test = [
         ("how to cut hair", 'pos'),
         ('w2express.com','neg'),
         ('how to play cornhole', 'pos'),
         ('safety ideas','neg'),
         ("check your claim status", 'pos'),
         ('buying rental cars','pos'),
         ('canon','neg'),
         ('changing your password','pos'),
         ('park central hotel convention center','neg'),         
         ('google','neg')     
    ]
    return train, test
    
def accuracy(train, test):
    cl = NaiveBayesClassifier(train)
    #print cl.classify("learn Python language")
    #prob_dist = cl.prob_classify("university of cauca")
    #print prob_dist.max()
    #print "Pos:", prob_dist.prob("pos")
    #print "Neg:", prob_dist.prob("neg")
    print "Accuracy: ", cl.accuracy(test)
    cl.show_informative_features(20)
    print
    return cl

def posTaggingCollection(train_file):
    postags_train = []
    for trf in train_file:        
        #print trf[0]
        data = []
        t = TextBlob(trf[0])
        postg = t.tags
        p = ''
        for pt in postg:
            p+= str(pt[1]) + " "
        #print p
        data.append(p)
        data.append(trf[1])
        postags_train.append(tuple(data))
    #print postags_train
    return postags_train

def posTaggingDocument(sentence):
    t = TextBlob(sentence)
    p = ''
    for pt in t.tags:
        p+= str(pt[1]) + " "
    return p

def test(query, classifier):
    p = posTaggingDocument(query)
    classifier.classify(p)
    prob_dist = classifier.prob_classify(p)
    print "Max Probability Distribution:", prob_dist.max()
    print "Pos:", prob_dist.prob("pos")
    print "Neg:", prob_dist.prob("neg")
    return prob_dist.max()

def updateClassifier(query, classifier, label):
    post = posTaggingDocument(query)
    new_data = [(post, label)]
    classifier.update(new_data)

    
    
        


    
