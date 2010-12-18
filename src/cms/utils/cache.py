#-*- coding: utf-8 -*-
'''
Created on 16 дек. 2010

@author: ivan
'''
from google.appengine.api import memcache
from cms.utils.twitter import TwitterTagCrawler

def get_or_put_cache(key):
    cache = memcache.get(key)
    if cache:
        return cache
    else:
        value = TwitterTagCrawler("foobnix", None, None).search()
        memcache.add(key=key, value=value, time=3600) 
        return value
        
def get_from_cache(menu_id, page_id, lang):
    cache = memcache.get(get_id(menu_id, page_id, lang))
    if cache:
        return cache
    else:
        return None
    
def flash_cache():
    memcache.flush_all()

def put_to_cache(menu_id, page_id, lang, content):
    id = get_id(menu_id, page_id, lang)
    memcache.add(key=id, value=content, time=3600)   
       
def get_id(menu_id, page_id, lang):
    if not menu_id:
        menu_id = "__"    
    if not page_id:
        page_id = "-1"        
    id = "%s_%s_%s" % (menu_id, page_id, lang)
    return id
