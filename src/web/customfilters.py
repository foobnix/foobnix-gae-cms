#-*- coding: utf-8 -*-
'''
Created on 5 дек. 2010

@author: ivan
'''
"""
Gravatar Support for Bloog
"""
__author__ = 'Matteo Crippa'

import md5

from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def gravatar(email):
    return md5.new(email).hexdigest()    
    
register.filter(gravatar)
