#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from google.appengine.ext import db

class MenuModel(db.Model):
    link_id = db.StringProperty(multiline=False)
    name_ru = db.StringProperty(multiline=False)
    name_en = db.StringProperty(multiline=False)
    layout = db.StringProperty(multiline=False)
    position = db.StringProperty(multiline=False)
    index = db.IntegerProperty()
    is_visible = db.BooleanProperty()
    
    
class EmailModel(db.Model):
    subject = db.StringProperty(multiline=False)
    send_from = db.StringProperty(multiline=False)
    send_to = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    message = db.TextProperty()
    status = db.StringProperty(multiline=False)
    attachments = db.StringProperty(multiline=False)

class PageModel(db.Model):
    title_ru = db.StringProperty(multiline=False)
    title_en = db.StringProperty(multiline=False)
    
    content_ru = db.TextProperty()
    content_en = db.TextProperty()
    
    is_comment = db.BooleanProperty()
    is_visible = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    fk_menu = db.StringProperty(multiline=False)
    
    index = db.IntegerProperty()
    

class ProductModel(db.Model):
    title = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=True)
    new_price = db.StringProperty(multiline=False)
    old_price = db.StringProperty(multiline=False)
    images = db.StringProperty(multiline=False)
    date = db.DateTimeProperty(auto_now_add=True)

class ImageModel(db.Model):
    title = db.StringProperty(multiline=False)
    content = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True) 
    
class CommentModel(db.Model):
    name = db.StringProperty(multiline=False)
    site = db.StringProperty(multiline=False)
    comment_ru = db.TextProperty()
    comment_en = db.TextProperty()    
    page = db.ReferenceProperty(PageModel)
    date = db.DateTimeProperty(auto_now_add=True)
    user_id = db.StringProperty(multiline=False)    

class PropertieModel(db.Model):
    name = db.StringProperty(multiline=False)
    value_ru = db.StringProperty(multiline=True)
    value_en = db.StringProperty(multiline=True)    
    date = db.DateTimeProperty(auto_now_add=True)  


class StatisticModel(db.Model):
    userUUID = db.StringProperty(multiline=False)
    host = db.StringProperty(multiline=False)
    date = db.DateProperty(auto_now_add=True)
    version = db.StringProperty(multiline=False)

class CommonStatisticModel(db.Model):    
    date = db.DateProperty(auto_now_add=True)
    count = db.IntegerProperty(default=1) 

