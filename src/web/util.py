#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from web.model import MenuModel, PageModel
from web.config import layouts
def prepare_glob_dict():
    menu_list = MenuModel().all()
    menu_list.order("-is_visible")
    menu_list.order("-position")
    menu_list.order("index")
    menu_list.fetch(50)
    
    page_list = PageModel().all()
    page_list.order("-is_visible")
    page_list.order("-date")
    page_list.fetch(50)
    
    glob_dict = {
     'menu_list':menu_list,
     'page_list':page_list
     }
    return glob_dict

def get_pages(menu_name):
    page = PageModel().all()
    page.filter("fk_menu", menu_name)
    return page

def get_menu_layout(menu_name):
    page = MenuModel().all()
    page.filter("link_id", menu_name)
    
    layout = layouts[0]
    
    if page.count() >= 1:
        layout = page[0].layout
        
    return layout
    
