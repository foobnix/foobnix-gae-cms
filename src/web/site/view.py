#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import os
from web.model import PageModel
from web.util import prepare_glob_dict, get_pages, get_menu_layout
from web.config import admin_menu

class ViewPage(webapp.RequestHandler):
    """param1 - menu name"""
    def get(self, menu_name, page_key_id=None):
        glob_dict = prepare_glob_dict()        

        if page_key_id:
            page = PageModel().get_by_id(int(page_key_id))
            layout = "view_page"
            glob_dict["page"] = page
        else:        
            pages = get_pages(menu_name)
            layout = get_menu_layout(menu_name)
            glob_dict["pages"] = pages
        
        glob_dict["admin_menu"] = admin_menu              
        glob_dict["active"] = menu_name
        
        path = os.path.join(os.path.dirname(__file__), layout + '.html')
        self.response.out.write(template.render(path, glob_dict))
