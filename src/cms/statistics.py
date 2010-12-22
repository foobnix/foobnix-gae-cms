#-*- coding: utf-8 -*-
'''
Created on 22 дек. 2010

@author: ivan
'''
from google.appengine.ext import webapp
from cms.model import StatisticModel, CommonStatisticModel
from cms.utils.properties import get_propertie
from datetime import datetime

class SubmitVersion(webapp.RequestHandler):
    def get(self):
        uuid = self.request.get('uuid')
        host = self.request.get('host')
        version = self.request.get('version')
        
        if not uuid or not host:
            return self.response.out.write(get_propertie("config.version"))
            
        find = StatisticModel().all()
        find.filter("userUUID", uuid)
        find.filter("host", host)
        find.filter("date", datetime.now().date())
        
        """if not hound uniq pc"""
        if find.count() == 0:
            nfind = CommonStatisticModel().all()                
            nfind.filter("date", datetime.now().date())
            
            
            if nfind.count() >= 1 :
                add = nfind[0]                
                add.count += 1
                add.put()    
            else:
                add = CommonStatisticModel()                                                
                add.put()

            model = StatisticModel()
            model.userUUID = uuid[:100]
            model.host = host[:100]
            model.version = version[:100]
            model.put()
                  
        self.response.out.write(get_propertie("config.version"))
