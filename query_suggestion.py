# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 09:17:47 2014

@author: javier
"""


import urllib2

def getgoogleurl(search,siteurl=False):
    if siteurl==False:
        return 'http://www.google.com/search?q='+urllib2.quote(search)+'&oq='+urllib2.quote(search)
    else:
        return 'http://www.google.com/search?q=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)+'&oq=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)

def getgooglelinks(search,siteurl=False):
   #google returns 403 without user agent
   headers = {'User-agent':'Mozilla/11.0'}
   req = urllib2.Request(getgoogleurl(search,siteurl),None,headers)
   site = urllib2.urlopen(req)
   data = site.read()
   site.close()

   #no beatifulsoup because google html is generated with javascript
   start = data.find('<div id="res">')
   end = data.find('<div id="foot">')
   if data[start:end]=='':
      #error, no links to find
      return False
   else:
      links =[]
      data = data[start:end]
      start = 0
      end = 0        
      while start>-1 and end>-1:
          #get only results of the provided site
          if siteurl==False:
            start = data.find('<a href="/url?q=')
          else:
            start = data.find('<a href="/url?q='+str(siteurl))
          data = data[start+len('<a href="/url?q='):]
          end = data.find('&amp;sa=U&amp;ei=')
          if start>-1 and end>-1: 
              link =  urllib2.unquote(data[0:end])
              data = data[end:len(data)]
              if link.find('http')==0:
                  links.append(link)
      return links

links = getgooglelinks('popayán','http://www.facebook.com/')
for link in links:
       print link

"""
from xgoogle.googlesets import GoogleSets
gs = GoogleSets(['python', 'perl'])
items = gs.get_results()
for item in items:
  print item.encode('utf8')
"""

""" MUY BUENO
import json
import urllib

def showsome(searchfor):
  query = urllib.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = urllib.urlopen(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  data = results['responseData']
  print 'Total results: %s' % data['cursor']['estimatedResultCount']
  hits = data['results']
  print 'Top %d hits:' % len(hits)
  for h in hits: print ' ', h['url']
  print 'For more results, see %s' % data['cursor']['moreResultsUrl']
  print
  for result in data['results']:
    #print result
    title = result['title']
    url = result['url']   # was URL in the original and that threw a name error exception
    content = result['content']
    print "Title:\t ", title
    print "Content:\t ", content
    print "Url:\t ", url
    print
    print

showsome('python')

"""

"""
from sgmllib import SGMLParser
import urllib2
import urllib

# Define the class that will parse the suggestion XML
class PullSuggestions(SGMLParser):

   def reset(self):
      SGMLParser.reset(self)
      self.suggestions = []
      self.queries = []

   def start_suggestion(self, attrs):
      for a in attrs:
         if a[0] == 'data': self.suggestions.append(a[1])

   def start_num_queries(self, attrs):
      for a in attrs:
         if a[0] == 'int': self.queries.append(a[1])


# -----------------------------------------------------------
# Enter your phrase here.  Be sure to leave the %s at the end!
# -----------------------------------------------------------
base_query = "unicauca %s"  #This is the base query

alphabet = "abcdefghijklmnopqrstuvwxyz"
for letter in alphabet:
   q = base_query % letter;
   query = urllib.urlencode({'q' : q})
   url = "http://google.com/complete/search?output=toolbar&%s" % query

   res = urllib2.urlopen(url)
   parser = PullSuggestions()
   parser.feed(res.read())
   parser.close()
   
   #print parser.suggestions
   #print 
   #print parser.queries
   
   for i in range(0,len(parser.suggestions)):
      print "%s\t%s" % (parser.suggestions[i], parser.queries)
"""

"""
from urllib import quote
from string import ascii_lowercase
from operator import itemgetter
import os
import random
import requests
from datetime import datetime
from lib.languages import LANGUAGES, get_language_by_name
from lib.utils import format_timedelta
 
try:
    import json
except ImportError:
    import simplejson as json
 
#Set the user agent to a common browser user agent string to get always utf-8 encoded response
headers = {'User-agent':'Mozilla/5.0'}
languages = sorted(LANGUAGES, key=itemgetter('name'))
#proxy_list = ['http://uberminiproxy.appspot.com/', 
            #'http://uberminiproxy-1.appspot.com/', 
            #'http://uberminiproxy-2.appspot.com/',
            #'http://uberminiproxy-3.appspot.com/',
            #'http://uberminiproxy-4.appspot.com/']
#Alternative URL
#www.google.com/complete/search?hjson=true&qu=a
 
def get_suggestion(query, lang, tld, ds=''):
    #"Query Google suggest service"
    suggestions = []
    if query:
        if isinstance(query, unicode): 
            query = query.encode('utf-8')
        query = quote(query)
        url = "http://clients1.google.%s/complete/search?hl=%s&q=%s&json=t&ds=%s&client=serp" %(tld, lang, query, ds)
        #the_url = random.choice(proxy_list)
        #response = requests.get(the_url, headers=headers, params={'url':url})
        response = requests.get(url, headers=headers)
        if response.ok:
            result = json.loads(response.content)
            suggestions = [i for i in result[1]]
        else:
            pass #FIXME handle and display errors
    return suggestions
 
def get_news_suggestion(query, lang, country):
    suggestions = []
    if query:
        if isinstance(query, unicode): 
            query = query.encode('utf-8')
        query = quote(query)
        url = "http://news.google.com/complete/search?hl=%s&gl=%s&ds=n&nolabels=t&hjson=t&client=news&q=%s" %(lang, country, query)
        #the_url = random.choice(proxy_list)
        #response = requests.get(the_url, headers=headers, params={'url':url})
        response = requests.get(url, headers=headers)
        if response.ok:
            result = json.loads(response.content)
            suggestions = [i[0] for i in result[1]]
    return suggestions
 
def single_suggest(query, lang, source):
    #"Provide suggestions via AJAX"
    result = []
    language = get_language_by_name(lang)
    if source == 'web':
        result = get_suggestion(query, language['code'], language['tld'])
    elif source == 'pr':
        result = get_suggestion(query, language['code'], language['tld'], ds='pr')
    elif source == 'news':
        result = get_news_suggestion(query, language['code'], language['country'])
    return result[1:]
 
def single_letter_recursive_suggest(query, language, source):
    #"Get suggestion and expand the query"
    
    selected_language = get_language_by_name(language)
    expansion = []
    chars = ascii_lowercase
    
    try:
        if source == 'web':
            gweb = get_suggestion(query, selected_language['code'], selected_language['tld'])
        elif source == 'pr':
            gweb = get_suggestion(query, selected_language['code'], selected_language['tld'], ds='pr')
        elif source == 'news':
            gweb = get_news_suggestion(query, selected_language['code'], selected_language['country'])
        for letter in chars:
            exp_query = query + ' ' + letter 
            if source == 'web':
                suggestions = get_suggestion(exp_query, selected_language['code'], selected_language['tld'])
            elif source == 'pr':
                suggestions = get_suggestion(query, selected_language['code'], selected_language['tld'], ds='pr')
            elif source == 'news':
                suggestions = get_news_suggestion(exp_query, selected_language['code'], selected_language['country'])
            if suggestions:
                expansion.append((letter, suggestions))
 
    except (IOError, ValueError), e:
        gweb = ''
        expansion = ''
    data = {'result':gweb, 'expansion':expansion, 'date':datetime.now()}
    code = selected_language['code']
    expansion_words = data['result']
    for ex in data['expansion']:
        expansion_words.extend(ex[1])
    return expansion_words
 
#Will this write the file - again
if __name__ == "__main__":
    print single_letter_recursive_suggest("patio door handle", "English/USA", "web")
    """