#-*- coding: utf-8 -*-
'''
Created on 21 дек. 2010

@author: ivan
'''
from cms.model import PropertieModel, MenuModel
from cms.admin_config import default_properties
from configuration import DEBUG

def add_menu(id, ru, eng, pos, bg):
    menu = MenuModel()
    menu.link_id = id
    menu.name_ru = ru
    menu.name_en = eng
    menu.position = pos
    menu.background = bg
    menu.put()

def populate_menu():
    all = MenuModel().all()
    for item in all:
        item.delete()
    add_menu("senin", "Сенин", "Senin", "TOP", "images/bg2.jpg")
    add_menu("contatcs", "Контакты", "Сontacts", "TOP", "images/bg3.jpg")
    add_menu("catalog", "Каталоr", "Catalog", "TOP", "images/bg_l.jpg")
    add_menu("restavration", "Реставрация", "Restavration", "TOP", "images/senin_51.jpg")
    

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
    
