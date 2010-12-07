#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import os
from google.appengine.api import mail
import re
from configuration import TEMPLATE_PATH
from cms.model import EmailModel
from cms.glob_dict import get_menu_by, prepare_glob_dict, get_pages, get_layout
from cms.admin_config import admin_menu

def is_valid_email(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False

class SendEmails(webapp.RequestHandler):
    def get(self, key_id):
        email = EmailModel().get_by_id(int(key_id))
        
        for to in re.split("[ ,\n\r]", email.send_to):
            if to and is_valid_email(to):
                email.status = "Send"
                mail.send_mail(
                      sender=email.send_from,
                      to=to,
                      subject=email.subject,
                      body=email.message)
        email.put()
        self.redirect("/admin/email")
   

class ViewPage(webapp.RequestHandler):
    """param1 - menu name"""
    def get(self, menu_link_id=None, page_key_id=None):
        glob_dict = prepare_glob_dict()        
        
        menu = get_menu_by(menu_link_id)
        if not menu:
            #result_layout = INDEX_TEMPLATE
            path = os.path.join(TEMPLATE_PATH, "base.html")            
            return self.response.out.write(template.render(path, glob_dict))
            
        
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
        
        path = os.path.join(TEMPLATE_PATH, result_layout)
        self.response.out.write(template.render(path, glob_dict))
