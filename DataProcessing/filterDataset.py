# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:00:00 2013

@author: javier
"""

"""
List of Part-of-Speech tags of Penn Treebank Project
<http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html>

VB    Verb, base form
VBD    Verb, past tense
VBG    Verb, gerund or present participle
VBN    Verb, past participle
VBP    Verb, non-3rd person singular present
VBZ    Verb, 3rd person singular present
WRB    Wh-adverb
"""

import time

#file_name = 'Data/rawTrainPosTags.txt'

def filterDataset(file_name, new_file):
    size = len(open(file_name).readlines())
    print size

    document = open(new_file, 'a')      
    #dataset = []    
    
    l = ''
    for line in open(file_name):
        if (line.strip(' \t\r\n') != l):
            #dataset.append(line.strip(' \t\r\n'))
            document.write(line.strip(' \t\r\n') + "\n")
            l = line.strip(' \t\r\n')  
            
    document.close 
    
    #print len(open(new_file).readlines())
    
    
def filterDatasetByVerb(file_name, new_file):
    t0 = time.clock()
    size = len(open(file_name).readlines())
    print size

    document = open(new_file, 'a')      
    
    for line in open(file_name):
        l = line.strip(' \t\r\n')        
        #if (l.find('V') == -1):  #Filter by Verb
        if (l.find('W') == -1):   #Filter by Wh-words 
            #print l
            document.write(l + "\n")    
            
    document.close     
    print "Filter by verbs done on", time.clock() - t0, "seconds."
            
        
