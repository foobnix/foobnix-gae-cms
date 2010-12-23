#-*- coding: utf-8 -*-
'''
Created on 23 дек. 2010

@author: ivan
'''
from google.appengine.ext import webapp
from cms.utils.twitter import TwitterTagCrawler
from cms.model import CommentModel, COMMENT_CATEGORY_TWITTER
class UpdateTwitters(webapp.RequestHandler):
    def get(self):                
        results = TwitterTagCrawler("foobnix").loop_search()
        for result  in results:
            all = CommentModel().all()
            all.filter("user_id", str(result['id']))
            if all.count() == 0:    
                model = CommentModel()
                model.comment_ru = result['text'] 
                model.comment_en = result['text']
                model.name = result['from_user']
                model.site = "http://twitter.com/" + result['from_user']
                model.category = COMMENT_CATEGORY_TWITTER
                model.user_id = str(result['id'])
                model.put()
        self.response.out.write("OK")
        
 
