# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 22:36:31 2014

@author: Javier Suarez
"""

import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.disabled = True

from gensim import corpora
import nltk as nl
from textblob import TextBlob
import nltk.corpus
import time
import chunker as chu
import chunker_noun as chn

class MyCorpus(object):
    def __iter__(self):
        
        t0 = time.clock()
        print "Generating dictionary, this takes some time, please wait..."
        
        data_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
        model_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
        data_file = "aolGoals.txt"   
        dictionary_name = "goal_dictionary.dict"
                
        # collect statistics about all tokens   
        dictionary = corpora.Dictionary(line.lower().split() for line in open(data_path + data_file))
        stopwords = set(nltk.corpus.stopwords.words('english'))
        stopwords.update(['pregnant', 'fuck', 'wife', 'fucking', 'up', 'free', 'baby', 'address', 'rid', 'space', 'name', 'pimp', 'porn', 'sex', 'myspace'])
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
        #stoplist = set('aol up from free out on for a of the and to in your an my i you he she it we they with how where'.split())
        # remove stop words and words that appear only once
        stop_ids = [dictionary.token2id[stopword] for stopword in stopwords if stopword in dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
        dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
        dictionary.compactify() # remove gaps in id sequence after words that were removed        
        dictionary.save(model_path + dictionary_name)
        
        for line in open(data_path + data_file):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())    
            
        print  "\tDictionary created on", time.clock() - t0, "seconds."
        print "\t",dictionary        
        

def MyNewCorpus(query):
    
    t0 = time.clock()
    print "Generating dictionary, this takes some time, please wait...!"
    
    data_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
    #model_path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/QueryAnalyzer/Models/"
    model_path = '/tmp/'
    data_file = "aolGoals.txt"   
    dictionary_name = "dictionary.dict"

    noun = []
    empty = []
    noun = chn.extract(query)
    if noun == empty:
        noun.append(query)
        
    print "noun", noun
    size  = len(noun)   
    #print size    
    goals = []
    #ln = [line.lower().split() for line in open(data_path + data_file)]
    if (size > 0):        
        for i in range(0, size):    
            word = " " + noun[i] + " "
            #print "--Word:", word            
            for line in open(data_path + data_file):
                if word in line: 
                    goals.append(line.strip(' \t\r\n'))
            #print"-->", len(goals)
    #print goals
    #print len(goals)
           
    # collect statistics about all tokens   
    dictionary = corpora.Dictionary(goal.lower().split() for goal in goals)
    stopwords = set(nltk.corpus.stopwords.words('english'))
    stopwords.update(['fuck', 'wife', 'fucking', 'rid', 'porn', 'sex', 'myspace', 'anal', 'penis', 'cum', '500', 'nj', 'va', 'tulsa'])
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
    #stoplist = set('aol up from free out on for a of the and to in your an my i you he she it we they with how where'.split())
    # remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stopwords if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 0]
    dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed            
    dictionary.save(model_path + dictionary_name)        
    
    for line in goals:
        # assume there's one document per line, tokens separated by whitespace
        yield dictionary.doc2bow(line.lower().split())    
    
    
    print  "\tDictionary created on", time.clock() - t0, "seconds."
    print "\t",dictionary      


def getCorpus(query):
    corpus = MyNewCorpus(query)
    model_path = "/tmp/"
    corpus_name = "corpus_2.mm"         
    dictionary_name = "dictionary.dict"
    corpora.MmCorpus.serialize(model_path + corpus_name, corpus)
    
    dictionary = corpora.Dictionary.load(model_path + dictionary_name)
    corpus = corpora.MmCorpus(model_path + corpus_name)
    
    return dictionary, corpus
    
#corpus = MyNewCorpus("Car")
#corpus = MyCorpus() # doesn't load the corpus into memory!
#corpus.__iter__()
# for vector in corpus_memory_friendly: # load one vector into memory at a time
# print vector
#path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
#corpora.MmCorpus.serialize(path + 'corpus_sample.mm', corpus)



