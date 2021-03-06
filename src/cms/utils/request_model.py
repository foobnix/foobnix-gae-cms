#-*- coding: utf-8 -*-
'''
Created on 16 дек. 2010

@author: ivan
'''
from configuration import CMS_LANGUAGES, LANG_CODE_DEFAULT
from cms.utils.translate import get_translated
from google.appengine.ext import db
from google.appengine.api import images
import datetime
from django.utils.html import escape

def safe_model(model):
    for properie in model.properties():
        db_type = model.properties()[properie]
        if type(db_type) == db.StringProperty or type(db_type) == db.TextProperty:
            value = getattr(model, properie)
            if value:
                safe = escape(value)
                setattr(model, properie, safe)
    return model

def request_to_model(model, request, prefix):
    if not model:
        return None
    for properie in model.properties():
        db_type = model.properties()[properie]
        request_propertrie = prefix + "." + properie
        request_value = request.get(request_propertrie)
        
        if not request_value and "_" in properie:
            name = properie[:-3]
            lang = properie[-2:]                
            if lang != LANG_CODE_DEFAULT and lang in CMS_LANGUAGES.keys():
                """translate"""
                origin = request.get(prefix + "." + name + "_" + LANG_CODE_DEFAULT)
                request_value = get_translated(origin, LANG_CODE_DEFAULT, lang)
        
        if type(db_type) == db.IntegerProperty:
            if not request_value:
                request_value = 0;
            setattr(model, properie, int(request_value))
        elif  type(db_type) == db.BooleanProperty:
            if not request_value:
                request_value = False;
            setattr(model, properie, bool(request_value))
        elif type(db_type) == db.DateTimeProperty:
            setattr(model, properie, datetime.datetime.utcnow())
        elif type(db_type) == db.BlobProperty:
            if request_value:                
                setattr(model, properie, db.Blob(request_value))
        elif type(db_type) == db.ReferenceProperty:
            pass             
        else:
            if hasattr(model, properie):    
                setattr(model, properie, request_value)
    return model
