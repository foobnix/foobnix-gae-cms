#-*- coding: utf-8 -*-
'''
Created on 5 дек. 2010

@author: ivan
'''

from google.appengine.ext import webapp
register = webapp.template.create_template_register()

@register.filter
def split(value, prefix):
    if not value:
        return []
    return value.split(prefix)
