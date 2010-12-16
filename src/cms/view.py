#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import os
from google.appengine.api import mail, users
import re
from configuration import TEMPLATE_PATH
from cms.model import EmailModel, ImageModel, CommentModel
from cms.glob_dict import get_menu_by, prepare_glob_dict, get_pages, get_layout, \
    get_default_menu_id
from cms.admin_config import admin_menu
from cms.admin import get_lang
from cms.utils.request_model import request_to_model
from appengine_utilities.sessions import Session
import uuid
from django.utils.html import urlize

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
                attachments = []
                if email.attachments:
                    list = email.attachments.split(",")
                    for id in list: 
                        image = ImageModel.get_by_id(int(id))
                        if image:
                            attachments.append((image.title + ".png", image.content))
                
                email.status = "Send"
                mail.send_mail(
                      sender=email.send_from,
                      to=to,
                      subject=email.subject,
                      body=email.message,
                      html=email.message,
                      attachments=attachments)
        email.put()
        self.redirect("/admin/email")
   

class ViewPage(webapp.RequestHandler):
    """param1 - menu name"""
    def post(self, menu_id=None, page_id=None):
        self.get(menu_id, page_id)
         
    def get(self, menu_id=None, page_id=None):
        lang = get_lang(self.request)
        
        
        session = Session()
        if not session.has_key('user_id'):
            session['user_id'] = uuid.uuid4().hex        
                
        if not menu_id:
            menu_id = get_default_menu_id()
        
        glob_dict = prepare_glob_dict()
        
        user = users.get_current_user()
        glob_dict["user"] = user
        
        if not self.request.get("mode"):
            glob_dict["mode"] = "debug"
        else:
            glob_dict["mode"] = self.request.get("mode")
            
        glob_dict["host"] = self.request.headers['Host']
        glob_dict["lang"] = lang
        glob_dict["session"] = session
                
        
        menu = get_menu_by(menu_id)
        if not menu:
            #result_layout = INDEX_TEMPLATE
            path = os.path.join(TEMPLATE_PATH, "base.html")            
            return self.response.out.write(template.render(path, glob_dict))
            
        
        layout = get_layout(menu.layout)
        
        if page_id:
            
            page = layout["model"].get_by_id(int(page_id))
            result_layout = layout["child_template"]
            glob_dict["item"] = page
            
            
            comments = CommentModel().all()
            comments.order("-date")
            comments.filter("page", page)
            glob_dict["comments"] = comments
            
            if self.request.get('action') == "delete":
                id = self.request.get('comment.key_id')
                comment = CommentModel().get_by_id(int(id))
                if comment  and comment.user_id == session['user_id']:
                    comment.delete()
                    self.redirect("/%s/%s" % (menu_id, page_id)) 
                                
            
            if self.request.get('action') == "addupdate":            
                comment = request_to_model(CommentModel(), self.request, "comment")
                comment.page = page
                
                correct = True
                if not comment.name:
                    comment.name_error = True
                    correct = False
                
                if not comment.comment_ru or not comment.comment_en:
                    comment.comment_error = True
                    correct = False
                else:
                    comment.comment_ru = urlize(comment.comment_ru)
                    comment.comment_en = urlize(comment.comment_en)
                    
                
                if not comment.site:
                    comment.site = "http://www.foobnix.com"
                
                if not comment.site.startswith("http://"):
                    comment.site = "http://" + comment.site  
                
                if correct:
                    comment.user_id = session['user_id']
                    comment.put()
                    self.redirect("/%s/%s" % (menu_id, page_id))
                
                glob_dict["comment"] = comment
                
                
            
        else:        
            pages = get_pages(menu_id)            
            glob_dict["pages"] = pages
            result_layout = layout["template"]
        
        glob_dict["admin_menu"] = admin_menu              
        glob_dict["active"] = menu_id        
        glob_dict["menu_id"] = menu_id
        glob_dict["page_id"] = page_id
        glob_dict["active_menu"] = get_menu_by(menu_id)
        
        glob_dict["content_right"] = template.render(os.path.join(TEMPLATE_PATH, "content_right.html"), glob_dict)
        
        path = os.path.join(TEMPLATE_PATH, result_layout)
        self.response.out.write(template.render(path, glob_dict))
