#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from cms.model import MenuModel, PageModel, EmailModel, ProductModel, ImageModel, \
    PropertieModel, CommentModel, COMMENT_CATEGORY_PAGE, \
    COMMENT_CATEGORY_TWITTER
from cms.admin_config import layouts, admin_menu
from configuration import CMS_LANGUAGES

def get_pages(menu_name=None):
    page_list = PageModel().all()
    page_list.order("-is_visible")
    page_list.order("fk_menu")
    page_list.order("index")
    page_list.order("-date")
    if menu_name:
        page_list.filter("fk_menu", menu_name)
    return page_list

def get_menus():
    menu_list = MenuModel().all()
    menu_list.order("-is_visible")
    menu_list.order("-parent_id")
    menu_list.order("-position")
    menu_list.order("index")
    return menu_list
    

def _prepare_glob_dict():
    email_list = EmailModel().all()
    email_list.order("-date")

    
    product_list = ProductModel().all()
    product_list.order("-date")
    
    images_list = ImageModel().all()
    images_list.order("-date")
    
    propertie_list = PropertieModel().all()
    propertie_list.order("-date")
    
    comment_list = CommentModel().all()
    comment_list.filter("category", COMMENT_CATEGORY_PAGE)
    comment_list.order("-date")
    
    twitter_list = CommentModel().all()
    twitter_list.filter("category", COMMENT_CATEGORY_TWITTER)
    twitter_list.order("-date")
    
    
    glob_dict = {
     'langs':CMS_LANGUAGES,
     'page_list':get_pages(),
     'menu_list':get_menus(),
     'email_list':email_list,
     'product_list':product_list,
     'comment_list':comment_list,
     'twitter_list':twitter_list,
     'image_list':images_list,
     'propertie_list':propertie_list,
      "admin_menu" : admin_menu
     }    
    return glob_dict

def prepare_glob_dict():
    return _prepare_glob_dict()

def get_layout(layout_id):
    if not layout_id:
        return layouts[0]
    
    for layout in layouts:
        if layout["id"] == layout_id:
            return layout
    return None 
        

def get_default_menu_id():   
    menu = get_menu_by(None)
    if menu:
        return menu.link_id
 
def get_menu_by(link_id):
    menu_list = get_menus()    
    if link_id:
        menu_list.filter("link_id", link_id)
        
    if menu_list.count() >= 1:
        return menu_list[0]
        
    return None
    
