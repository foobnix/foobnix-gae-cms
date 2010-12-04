#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from google.appengine.ext import db
class MenuModel(db.Model):
    link_id = db.StringProperty(multiline=False)
    name = db.StringProperty(multiline=False)
    layout = db.StringProperty(multiline=False)
    position = db.StringProperty(multiline=False)
    index = db.IntegerProperty()
    is_visible = db.BooleanProperty()
    
    def get_name(self):
        return "menu"

class PageModel(db.Model):
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    is_comment = db.BooleanProperty()
    is_visible = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    fk_menu = db.StringProperty(multiline=False)
    
    def get_name(self):
        return "page"

