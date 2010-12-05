from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from web.config import admin_menu, layouts, positions, CMS_URL, CMS_EDIT, \
    CMS_VIEW
from web.util import prepare_glob_dict

class ViewEditAdminPage():
    def __init__(self, handler, admin_model, glob_dict):
        self.request = handler.request
        self.redirect = handler.redirect
        self.response = handler.response
        self.glob_dict = glob_dict
        self.admin_model = admin_model
        
    def proccess(self):
        template_dict = self.admin_model["template_dict"]
        self.model = self.admin_model["model"]
        
        if self.request.get('action') == "edit":
            key_id = self.request.get(template_dict + '.key_id')
            db_model = None
            if key_id:
                db_model = self.model.get_by_id(int(key_id))

            if not db_model:
                db_model = self.request_to_model(self.admin_model["model"], self.request, template_dict)
                db_model.put()
                
            self.glob_dict[template_dict] = db_model
            
                        
        elif self.request.get('action') == "addupdate":
            key_id = self.request.get(template_dict + '.key_id')
            if key_id:
                db_model = self.model.get_by_id(int(key_id))
            else:
                db_model = self.admin_model["model"]
            add = self.request_to_model(db_model, self.request, template_dict)
            add.put()
            self.glob_dict[template_dict] = add
            
        elif self.request.get('action') == "delete":
            key_id = self.request.get(template_dict + '.key_id')
            model = self.model.get_by_id(int(key_id))
            if model:
                model.delete()
             
            self.redirect(self.admin_model["link_id"])
            return None
        
        path = os.path.join(os.path.dirname(__file__), self.admin_model["template"])
        self.response.out.write(template.render(path, self.glob_dict))
    
    def request_to_model(self, model, request, prefix):
        for properie in model.properties():
            db_type = model.properties()[properie]
            request_propertrie = prefix + "." + properie
            request_value = request.get(request_propertrie)
            
            #if getattr(model, properie):
            #    continue;             
            
            if type(db_type) == db.IntegerProperty:
                if not request_value:
                    request_value = 0;
                setattr(model, properie, int(request_value))
            elif  type(db_type) == db.BooleanProperty:
                if not request_value:
                    request_value = False;
                setattr(model, properie, bool(request_value))
            elif type(db_type) == db.DateTimeProperty:
                pass
            else:
                setattr(model, properie, request_value)
        return model

class AdminPage(webapp.RequestHandler):
    """param1 - menu name"""
    def get(self, admin_page=None):
        glob_dict = prepare_glob_dict()
        glob_dict["admin_menu"] = admin_menu
        glob_dict["layouts"] = layouts
        glob_dict["positions"] = positions
        
        find = False
        for admin_model in admin_menu:
            page_link = admin_model["link_id"][len(CMS_URL) + 1:]
            if page_link == admin_page:
                find = True
                glob_dict["admin_model"] = admin_model
                
                if admin_model["type"] == CMS_EDIT:            
                    page = ViewEditAdminPage(self, admin_model, glob_dict)
                    page.proccess()
                elif admin_model["type"] == CMS_VIEW:
                    path = os.path.join(os.path.dirname(__file__), admin_model["template"])
                    self.response.out.write(template.render(path, glob_dict))
        if not find:
            path = os.path.join(os.path.dirname(__file__), 'admin.html')
            self.response.out.write(template.render(path, glob_dict))
