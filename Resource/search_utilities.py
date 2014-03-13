# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 09:17:47 2014

@author: javier
"""

import json
import urllib
import urllib2
from sgmllib import SGMLParser
from xgoogle.search import GoogleSearch, SearchError


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


def searchByQueryAndURL(query, url):
    links = getgooglelinks(query,url)
    l = []
    for link in links:
        print link
        l.append(link)
    return l


def searchByXGoogle(query):
    try:
        gs = GoogleSearch("quick and dirty")
        gs.results_per_page = 50
        results = gs.get_results()
        for res in results:
            print
            print "Title: \t", res.title.encode('utf8')
            print "Descr: \t", res.desc.encode('utf8')
            print "URL: \t", res.url.encode('utf8')
            print     
            
    except SearchError, e:
         print "Search failed: %s" % e    


def showSome(searchfor):
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

def suggestions(request):
    # -----------------------------------------------------------
    # Enter your phrase here.  Be sure to leave the %s at the end!
    # -----------------------------------------------------------
    base_query = request + " %s"  #This is the base query
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter in alphabet:
       q = base_query % letter;
       query = urllib.urlencode({'q' : q})
       url = "http://google.com/complete/search?output=toolbar&%s" % query
    
       res = urllib2.urlopen(url)
       parser = PullSuggestions()
       parser.feed(res.read())
       parser.close()
       
       for i in range(0,len(parser.suggestions)):
          print "%s\t%s" % (parser.suggestions[i], parser.queries)


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
