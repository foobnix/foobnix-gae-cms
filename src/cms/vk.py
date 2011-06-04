#-*- coding: utf-8 -*-
'''
Created on 28 мая 2011

@author: ivan
'''
from google.appengine.ext import webapp
from cms.utils.properties import get_propertie, get_properties
class VkUserPass(webapp.RequestHandler):
    def get(self):
        self.response.out.write(get_propertie("vk.user") + ":" + get_propertie("vk.pass"))
    
    def post(self):
        self.response.out.write(get_propertie("vk.user") + ":" + get_properties("vk.pass").value_en)

        
