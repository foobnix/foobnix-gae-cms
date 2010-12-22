#-*- coding: utf-8 -*-

import httplib
import logging
import urllib
import simplejson
import time
 
SEARCH_HOST = "search.twitter.com"
SEARCH_PATH = "/search.json"
 
 
class TwitterTagCrawler(object):
    ''' Crawl twitter search API for matches to specified tag.  Use since_id to
    hopefully not submit the same message twice.  However, bug reports indicate
    since_id is not always reliable, and so we probably want to de-dup ourselves
    at some level '''
 
    def __init__(self, tag, max_id=None, interval=None):
        self.max_id = max_id
        self.tag = tag
        self.interval = interval
 
    def _search(self):
        c = httplib.HTTPConnection(SEARCH_HOST)
        params = {'q' : self.tag}
        path = "%s?%s" % (SEARCH_PATH, urllib.urlencode(params))
        try:
            c.request('GET', path)
            r = c.getresponse()
            data = r.read()
            c.close()            
            result = simplejson.loads(data)
            if result.has_key('result'):          
                return result['results']
        except Exception, e:
            logging.error("search() error: %s" % (e))
            
    
    def search(self):
        result = None
        for i in xrange(2):
            if not result:
                result = self._search()
                time.sleep(0.2)
            else:
                return result
        return result
                
                
            
        
