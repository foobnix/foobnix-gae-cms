#-*- coding: utf-8 -*-
'''
Created on 21 дек. 2010

@author: ivan
'''
from cms.model import PropertieModel
from cms.admin_config import default_properties
from configuration import DEBUG
def populate_properties():
    if DEBUG:
        all = PropertieModel().all()
        for item in all:
            item.delete()
        
    for propertie in default_properties:        
        model = PropertieModel().all()
        model.filter("name", propertie["name"])
        
        if model.count() == 0:
            new = PropertieModel()
            new.name = propertie["name"]
            new.value_ru = propertie["value_ru"]
            new.value_en = propertie["value_en"]
            new.put()

def get_propertie(name):
    model = PropertieModel().all()
    model.filter("name", name)
    return model.get().value_ru
    
