#-*- coding: utf-8 -*-

from google.appengine.ext import webapp
import os
from cms.admin_config import admin_menu, positions, CMS_URL, CMS_EDIT, \
    CMS_VIEW, layouts, IMAGE_NOT_FOUND
from cms.glob_dict import prepare_glob_dict
import copy
from cms.model import ImageModel, CommonStatisticModel, EmailStatisticModel
from google.appengine.api import users, memcache
from configuration import ADMIN_TEMPLATE_PATH, LANG_CODE_DEFAULT, CMS_CFG
from cms.login import check_user_admin
import logging
from cms.utils.request_model import request_to_model
from cms.utils.cache import flash_cache
from google.appengine.ext.webapp import template


class ViewImage (webapp.RequestHandler):
    def get(self, image_key_id, name=None):
        try:
            model = memcache.get(image_key_id)                
            if not model:                
                model = ImageModel().get_by_id(int(image_key_id))                
                memcache.add(key=image_key_id, value=model, time=CMS_CFG["cache_time"])            
        except Exception, e:
            logging.error(e)
            self.redirect(IMAGE_NOT_FOUND)
            return
            
            
        if model:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(model.content)
        else:
            self.redirect(IMAGE_NOT_FOUND)
class ViewEditAdminPage():
    def __init__(self, handler, admin_model):
        self.request = handler.request
        self.redirect = handler.redirect
        self.response = handler.response
        self.admin_model = admin_model
        
    def proccess(self, glob_dict):
        template_dict = self.admin_model["template_dict"]
        
        if template_dict == "statistic":
            glob_dict['stats'] = CommonStatisticModel().all().order("-date").fetch(30)
        
        if template_dict == "email_statistic":
            glob_dict['stats'] = EmailStatisticModel().all().order("-date").fetch(50)
        
        clean_model = copy.copy(self.admin_model["model"])
        
        items = clean_model.all()
        
        if hasattr(clean_model, "date"):
            items.order("-date")
        items.fetch(50)
            
        glob_dict["items"] = items 
        
        if self.request.get('action') == "edit":
            key_id = self.request.get(template_dict + '.key_id')
            db_model = None
            if key_id:
                db_model = clean_model.get_by_id(int(key_id))

            if not db_model:
                db_model = request_to_model(clean_model, self.request, template_dict)
                db_model.put()
                
            glob_dict[template_dict] = db_model
            
                        
        elif self.request.get('action') == "addupdate":
            key_id = self.request.get(template_dict + '.key_id')
            if key_id:
                db_model = clean_model.get_by_id(int(key_id))
            else:
                db_model = clean_model                
            add = request_to_model(db_model, self.request, template_dict)
            add.put()
            glob_dict[template_dict] = add
            
        elif self.request.get('action') == "delete":
            key_id = self.request.get(template_dict + '.key_id')
            model = clean_model.get_by_id(int(key_id))
            if model:
                model.delete()
             
            self.redirect(self.admin_model["link_id"])
            return None
        else:
            glob_dict[template_dict] = ""
        
        path = os.path.join(ADMIN_TEMPLATE_PATH, self.admin_model["template"])
        return template.render(path, glob_dict)
                
   
def get_lang(request):
    if request.get("lang"):
        return request.get("lang") 
    else:
        return LANG_CODE_DEFAULT

class AdminPage(webapp.RequestHandler):
    """param1 - menu name"""
    def post(self, admin_page=None):
        self.get(admin_page)
        
    def get(self, admin_page=None):
        user = users.get_current_user()
        check_user_admin(self, user)
        
        flash_cache()
        
        lang = get_lang(self.request)
        
        glob_dict = prepare_glob_dict()
        glob_dict['logout'] = users.create_logout_url(self.request.path)
        glob_dict["user"] = user
        glob_dict["lang"] = lang
        glob_dict["layouts"] = layouts
        glob_dict["positions"] = positions
        glob_dict["host"] = self.request.headers['Host']
        
        glob_dict["mode"] = "debug"
        
        
        find = False
        for admin_model in admin_menu:
            page_link = admin_model["link_id"][len(CMS_URL) + 1:]
            if page_link == admin_page:
                find = True
                glob_dict["admin_model"] = admin_model
                
                if admin_model["type"] == CMS_EDIT:            
                    page = ViewEditAdminPage(self, admin_model)
                    self.response.out.write(page.proccess(glob_dict))
                elif admin_model["type"] == CMS_VIEW:
                    path = os.path.join(ADMIN_TEMPLATE_PATH, admin_model["template"])
                    self.response.out.write(template.render(path, glob_dict))
        if not find:
            path = os.path.join(ADMIN_TEMPLATE_PATH, 'admin.html')
            self.response.out.write(template.render(path, glob_dict))

