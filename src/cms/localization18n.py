#-*- coding: utf-8 -*-
'''
Created on 7 дек. 2010

@author: ivan
'''
from configuration import ADMIN_TEMPLATE_PATH
import ConfigParser
import os

    
class Resources():
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(os.path.join(ADMIN_TEMPLATE_PATH, "resource", "resources.properties"))
    
    def get(self, param):
        return self.config.get('app', param)

    
        
 
