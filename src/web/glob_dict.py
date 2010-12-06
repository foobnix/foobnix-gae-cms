#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from web.model import MenuModel, PageModel, EmailModel, ProductModel, ImageModel
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
    
    email_list = EmailModel().all()
    email_list.order("-date")
    email_list.fetch(50)
    
    product_list = ProductModel().all()
    product_list.order("-date")
    product_list.fetch(50)
    
    images_list = ImageModel().all()
    images_list.order("-date")
    images_list.fetch(50)
    
    glob_dict = {
     'menu_list':menu_list,
     'page_list':page_list,
     'email_list':email_list,
     'product_list':product_list,
     'image_list':images_list
     }
    return glob_dict

def get_layout(layout_id):
    if not layout_id:
        return layouts[0]
    
    for layout in layouts:
        if layout["id"] == layout_id:
            return layout
    return None 
        

def get_pages(menu_name):
    page = PageModel().all()
    page.filter("fk_menu", menu_name)
    return page


def get_menu_by(link_id):
    page = MenuModel().all()
    if link_id:
        page.filter("link_id", link_id)
    
    if page.count() >= 1:
        return page[0]
        
    return None
    
