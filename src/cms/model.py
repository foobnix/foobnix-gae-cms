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
    parent_id = db.StringProperty(multiline=False)
    index = db.IntegerProperty()
    is_visible = db.BooleanProperty()
    background = db.StringProperty(multiline=False)
    

class EmailStatisticModel(db.Model):
    send_to = db.StringProperty(multiline=False)
    subject = db.StringProperty(multiline=False)
    status = db.StringProperty(multiline=False)
    count = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class EmailModel(db.Model):
    subject = db.StringProperty(multiline=False)
    send_from = db.StringProperty(multiline=False)
    
    send_to = db.TextProperty()
    
    date = db.DateTimeProperty(auto_now_add=True)
    message = db.TextProperty()
    status = db.StringProperty(multiline=False)
    statistics = db.TextProperty()
    attachments = db.StringProperty(multiline=False)



class PageModel(db.Model):
    link_id = db.StringProperty(multiline=False)
    description_ru = db.StringProperty(multiline=False)
    description_en = db.StringProperty(multiline=False)
    
    keywords_ru = db.StringProperty(multiline=False)
    keywords_en = db.StringProperty(multiline=False)
    
    title_ru = db.StringProperty(multiline=False)
    title_en = db.StringProperty(multiline=False)
    
    head_ru = db.TextProperty()
    head_en = db.TextProperty()
    
    content_ru = db.TextProperty()
    content_en = db.TextProperty()
    
    is_comment = db.BooleanProperty()
    is_visible = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    fk_menu = db.StringProperty(multiline=False)
    
    index = db.IntegerProperty()    
    image = db.StringProperty(multiline=False)
    

class ProductModel(db.Model):
    title = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=True)
    new_price = db.StringProperty(multiline=False)
    old_price = db.StringProperty(multiline=False)
    images = db.StringProperty(multiline=False)
    image_path = db.StringProperty(multiline=False)
    catalog_path = db.StringProperty(multiline=False)
    date = db.DateTimeProperty(auto_now_add=True)

class ImageModel(db.Model):
    title = db.StringProperty(multiline=False)
    content = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True) 
    
COMMENT_CATEGORY_TWITTER = "twitter"
COMMENT_CATEGORY_PAGE = "page"     
class CommentModel(db.Model):
    name = db.StringProperty(multiline=False)
    site = db.StringProperty(multiline=False)
    comment_ru = db.TextProperty()
    comment_en = db.TextProperty()   
    category = db.StringProperty(multiline=False)
    page = db.ReferenceProperty(PageModel)
    date = db.DateTimeProperty(auto_now_add=True)
    user_id = db.StringProperty(multiline=False)
    ip = db.StringProperty(multiline=False)    

class PropertieModel(db.Model):
    name = db.StringProperty(multiline=False)
    value_ru = db.StringProperty(multiline=True)
    value_en = db.StringProperty(multiline=True)    
    date = db.DateTimeProperty(auto_now_add=True)  


class StatisticModel(db.Model):
    userUUID = db.StringProperty(multiline=False)
    host = db.StringProperty(multiline=False)
    platform = db.StringProperty(multiline=False)
    date = db.DateProperty(auto_now_add=True)
    version = db.StringProperty(multiline=False)

class CommonStatisticModel(db.Model):    
    date = db.DateProperty(auto_now_add=True)
    count = db.IntegerProperty(default=1) 

