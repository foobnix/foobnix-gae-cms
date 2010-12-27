#-*- coding: utf-8 -*-
'''
Created on 5 дек. 2010

@author: ivan
'''

from google.appengine.ext import webapp
from cms.admin_config import IMAGE_NOT_FOUND
register = webapp.template.create_template_register()

@register.filter
def split(value, prefix=","):
    if not value:
        return []

    list = value.split(prefix)
    filtered = []
    for line in list:
        line = line.strip() 
        if line:
            filtered.append(line)
        
    return filtered

@register.filter
def first_image(value):
    list = split(value, ",")
    if list:
        return list[0]
    else:
        return IMAGE_NOT_FOUND
    
