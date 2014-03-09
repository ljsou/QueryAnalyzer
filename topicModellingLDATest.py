# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:02:13 2014

@author: javier
"""
#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from itertools import chain


path = "/media/University/UniversityDisc/2-Master/MasterThesis/EjecucionTesis/Desarrollo/PythonProjects/Data/"

dictionary = corpora.Dictionary.load(path + 'goal_sample_dictionary.dict')
corpus = corpora.MmCorpus(path + 'corpus_sample.mm')
print corpus

# extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
lda = models.LdaModel(corpus, id2word=dictionary, num_topics=100, update_every=1, chunksize=10000, passes=1) # initialize an LSI transformation
#corpus_lda = lda[corpus] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
print lda.show_topics(topics=10, topn=10, log=False, formatted=False)
print lda.print_topic(1, topn=3)

lda_corpus = lda[corpus]
print lda_corpus
scores = list(chain(*[[score for topic,score in topic] \
                      for topic in [doc for doc in lda_corpus]]))            
print len(scores)

threshold = sum(scores)/len(scores)
print "threshold", threshold
print

file_name = "aolGoalsSample.txt" 
documents = open(path + file_name)
for i,j in zip(lda_corpus,documents):
    for sc,t in i:
        print sc, " ", t, " ", j


doc = "find address with telephone number for free"
vec_bow = dictionary.doc2bow(doc.lower().split())
print "vec: ",  vec_bow
vec_lda = lda[vec_bow] # convert the query to LSI space
print "Result", vec_lda
print "Result", vec_lda[0][0]
print dictionary.token2id
print lda.show_topic(topicid=vec_lda[0][0], topn=3)

    


