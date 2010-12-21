#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from cms.model import MenuModel, PageModel, EmailModel, ProductModel, ImageModel, \
    PropertieModel, CommentModel
from cms.admin_config import layouts, admin_menu
from configuration import CMS_LANGUAGES
from cms.utils.twitter import TwitterTagCrawler
from cms.utils.cache import get_or_put_cache

def twits():
    return TwitterTagCrawler("foobnix", None, None).search()

def prepare_glob_dict():
    menu_list = MenuModel().all()
    menu_list.order("-is_visible")
    menu_list.order("-position")
    menu_list.order("index")
    
    page_list = PageModel().all()
    page_list.order("-is_visible")
    page_list.order("fk_menu")
    page_list.order("-index")

    
    email_list = EmailModel().all()
    email_list.order("-date")

    
    product_list = ProductModel().all()
    product_list.order("-date")
    
    images_list = ImageModel().all()
    images_list.order("-date")
    
    propertie_list = PropertieModel().all()
    propertie_list.order("-date")
    
    comment_list = CommentModel().all()
    comment_list.order("-date")
    
    
    glob_dict = {
     'twitters':get_or_put_cache("twitters", twits),
     'langs':CMS_LANGUAGES,
     'page_list':page_list,
     'menu_list':menu_list,
     'email_list':email_list,
     'product_list':product_list,
     'comment_list':comment_list,
     'image_list':images_list,
     'propertie_list':propertie_list,
      "admin_menu" : admin_menu
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
    page.order("index")
    page.filter("fk_menu", menu_name)
    return page


def get_default_menu_id():   
    menu = get_menu_by(None)
    if menu:
        return menu.link_id
 
def get_menu_by(link_id):
    menu_list = MenuModel().all()    
    if not link_id:
            menu_list.order("-is_visible")
            menu_list.order("-position")
            menu_list.order("index")
    else:
        menu_list.filter("link_id", link_id)
        
    if menu_list.count() >= 1:
        return menu_list[0]
        
    return None
    
