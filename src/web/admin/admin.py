from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from web.config import admin_menu, layouts, positions
from web.util import prepare_glob_dict
from web.model import MenuModel, PageModel

class ViewEditAdminPage():
    def __init__(self, handler, model, glob_dict):
        self.parent_page = "admin"
        self.request = handler.request
        self.redirect = handler.redirect
        self.response = handler.response
        self.glob_dict = glob_dict
        self.model = model
        self.name = model.get_name()
        
        self.glob_dict["parent"] = self.parent_page
        self.glob_dict["name"] = self.name
        
    def proccess(self):
        if self.request.get('action') == "edit":
            key_id = self.request.get(self.name + '.key_id')
            db_model = None
            if key_id:
                db_model = self.model.get_by_id(int(key_id))

            if not db_model:
                db_model = self.request_to_model(self.model, self.request)
                db_model.put()
                
            self.glob_dict[self.name] = db_model
            
                        
        elif self.request.get('action') == "addupdate":
            key_id = self.request.get(self.name + '.key_id')
            if key_id:
                db_model = self.model.get_by_id(int(key_id))
            else:
                db_model = self.model
            add = self.request_to_model(db_model, self.request)
            add.put()
            self.glob_dict[self.name] = add
            #self.redirect("/%s/%s" % (self.parent_page, self.name))
            
        elif self.request.get('action') == "delete":
            key_id = self.request.get(self.name + '.key_id')
            model = self.model.get_by_id(int(key_id))
            if model:
                model.delete()
                
            self.redirect("/%s/%s" % (self.parent_page, self.name))
        
        path = os.path.join(os.path.dirname(__file__), '%s-%s.html' % (self.parent_page, self.name))
        self.response.out.write(template.render(path, self.glob_dict))
    
    def request_to_model(self, model, request):
        for properie in model.properties():
            db_type = model.properties()[properie]
            request_propertrie = model.get_name() + "." + properie
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
        
        if admin_page == "menu": 
            page = ViewEditAdminPage(self, MenuModel(), glob_dict)
            page.proccess()
        elif admin_page == "page":       
            view_menu = ViewEditAdminPage(self, PageModel(), glob_dict)
            view_menu.proccess()
        elif admin_page == "editor":       
            path = os.path.join(os.path.dirname(__file__), 'admin-editor.html')
            self.response.out.write(template.render(path, glob_dict))
        else:
            path = os.path.join(os.path.dirname(__file__), 'admin.html')
            self.response.out.write(template.render(path, glob_dict))
