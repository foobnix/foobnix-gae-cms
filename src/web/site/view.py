#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import os
from web.config import admin_menu
from web.glob_dict import prepare_glob_dict, get_pages, get_menu_by, get_layout

class ViewPage(webapp.RequestHandler):
    """param1 - menu name"""
    def get(self, menu_link_id, page_key_id=None):
        glob_dict = prepare_glob_dict()        
        
        menu = get_menu_by(menu_link_id)
        layout = get_layout(menu.layout)
        
        if page_key_id:
            
            page = layout["model"].get_by_id(int(page_key_id))
            result_layout = layout["child_template"]
            glob_dict["item"] = page
        else:        
            pages = get_pages(menu_link_id)            
            glob_dict["pages"] = pages
            result_layout = layout["template"]
        
        glob_dict["admin_menu"] = admin_menu              
        glob_dict["active"] = menu_link_id        
        glob_dict["active_menu"] = get_menu_by(menu_link_id)
        
        path = os.path.join(os.path.dirname(__file__), result_layout)
        self.response.out.write(template.render(path, glob_dict))
