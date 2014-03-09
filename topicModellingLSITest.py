# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:02:13 2014

@author: javier
"""
import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.disabled = False

from gensim import corpora, models, similarities
from itertools import chain

class MyCorpus(object):
    def __iter__(self):
        path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
        file_name = "aolGoalsSample.txt"   
        # collect statistics about all tokens   
        dictionary = corpora.Dictionary(line.lower().split() for line in open(path + file_name))
        stoplist = set('for a of the and to in your an my i you he she it we they with how'.split())
        # remove stop words and words that appear only once
        stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
        dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
        dictionary.compactify() # remove gaps in id sequence after words that were removed
        dictionary.save(path + 'goal_sample_dictionary.dict')
        print dictionary        
        
        for line in open(path + file_name):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())

#corpus = MyCorpus() # doesn't load the corpus into memory!
#print corpus
#for vector in corpus: # load one vector into memory at a time
#   print "v: ", vector
path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"
#One of the more notable file formats is the Market Matrix format. 
#To save a corpus in the Matrix Market format:
#corpora.MmCorpus.serialize(path + 'corpus_sample.mm', corpus)

"""
---------------------------------------------------------------------------------------
"""

dictionary = corpora.Dictionary.load(path + 'goal_sample_dictionary.dict')
#print list(dictionary)

corpus = corpora.MmCorpus(path + 'corpus_sample.mm')
print corpus

tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
doc_bow = [(0, 1), (1, 1)]
print tfidf[doc_bow] # step 2 -- use the model to transform vectors

corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print doc
    
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=4) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi


for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
    print doc


doc = "find address with telephone number for free"
vec_bow = dictionary.doc2bow(doc.lower().split())
print "vec: ",  vec_bow
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print dictionary.token2id

print lsi.show_topics(num_topics=2, num_words=5, log=False, formatted=False)
print lsi.print_topic(1, topn=3)

lsi_corpus = lsi[corpus]
print lsi

scores = list(chain(*[[score for topic,score in topic] \
                      for topic in [doc for doc in lsi_corpus]]))            
print len(scores)

threshold = sum(scores)/len(scores)
print "threshold", threshold
print

file_name = "aolGoalsSample.txt" 
documents = open(path + file_name)
for i,j in zip(lsi_corpus,documents):
    for sc,t in i:
        print sc, " ", t, " ", j
    


