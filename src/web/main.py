from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

positions = ["TOP", "LEFT"]
layouts = ["page", "download", "welcome"]

class MenuModel(db.Model):
    link_id = db.StringProperty(multiline=False)
    name = db.StringProperty(multiline=False)
    layout = db.StringProperty(multiline=False)
    position = db.StringProperty(multiline=False)
    index = db.IntegerProperty()
    is_visible = db.BooleanProperty()

class PageModel(db.Model):
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    is_comment = db.BooleanProperty()
    is_visible = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    fk_menu = db.StringProperty(multiline=False)       

admin_menu = [
        {"id":"/admin/emenu", "text":"eMenus", "template":"admin-emenu.html"},
        {"id":"/admin/epages", "text":"ePages", "template":"admin-epage.html"},
        {"id":"/admin/esettings", "text":"eSettins", "template":"admin-settings.html"}
        ]

def request_to_model(model, request, prefix="menu"):
    for properie in model.properties():
        db_type = model.properties()[properie]
        request_propertrie = prefix + "." + properie
        request_value = request.get(request_propertrie)
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

def get_active_page(*params):
    result = ""
    for param in params:
        if param:
            result = result + "/" + param
    return result

class AdminController():
    def __init__(self, param1, param2, request, redirect):
        self.response = None
        if param1 != "admin":
            return None

        values = {               
         'admin_menu':admin_menu,
         'param1':param1,
         'param2':param2,
         'layouts':layouts,
         'positions':positions,
         
         'active':get_active_page(param1, param2),
         }
        tpl = "admin"
        if param2 == "emenu":
            
            menu_list = MenuModel().all()
            menu_list.order("-is_visible")
            menu_list.order("-position")
            menu_list.order("index")
            menu_list.fetch(50)

            values["menu_list"] = menu_list
            
            tpl = "admin-emenu"
            
            if request.get('action') == "edit":
                key_id = request.get('key_id')
                menu = MenuModel.get_by_id(int(key_id))
                values["menu"] = menu
                            
            if request.get('action') == "addupdate":
                key_id = request.get('key_id')
                if key_id:
                    menu = MenuModel.get_by_id(int(key_id))
                else:
                    menu = MenuModel()
                add = request_to_model(menu, request, "menu")
                add.put()
                
                redirect(get_active_page(param1, param2))
            if request.get('action') == "delete":
                key_id = request.get('key_id')
                model = MenuModel.get_by_id(int(key_id))
                if model:
                    model.delete()
                redirect(get_active_page(param1, param2))
            
            
        if param2 == "epages":
            tpl = "admin-epages"
            
            page_list = PageModel().all()
            page_list.order("-is_visible")
            page_list.order("-date")
            page_list.fetch(50)
            
            menu_list = MenuModel().all()
            menu_list.order("index")
            menu_list.filter("is_visible", True)
            
            values["page_list"] = page_list
            values["menu_list"] = menu_list
            
            if request.get('action') == "edit":
                key_id = request.get('key_id')
                model = PageModel.get_by_id(int(key_id))
                values["page"] = model
                            
            if request.get('action') == "addupdate":
                key_id = request.get('key_id')
                if key_id:
                    model = PageModel.get_by_id(int(key_id))
                else:
                    model = PageModel()
                add = request_to_model(model, request, "page")
                add.put()
                
                redirect(get_active_page(param1, param2))
            if request.get('action') == "delete":
                key_id = request.get('key_id')
                model = PageModel.get_by_id(int(key_id))
                if model:
                    model.delete()
                redirect(get_active_page(param1, param2))
    
        path = os.path.join(os.path.dirname(__file__), tpl + '.html')
        self.response = template.render(path, values)
        
    def get_response(self):
        return self.response
            

class IndexPage(webapp.RequestHandler):
    def get(self, param1=None, param2=None):
        
        admin = AdminController(param1, param2, self.request, self.redirect)
        
        menu_list = MenuModel().all()
        menu_list.order("index")
        menu_list.fetch(50)
        #menu_list.filter("position", "TOP")
         
        values = {                  
                 'menu':menu_list,
                 'admin_menu':admin_menu,
                 'param1':param1,
                 'param2':param2,
                 'active':get_active_page(param1, param2),
                 'container':admin.get_response()
                 }
        
        path = os.path.join(os.path.dirname(__file__), 'template.html')
        self.response.out.write(template.render(path, values))

application = webapp.WSGIApplication([
                                      (r'/(.*)/(.*)/', IndexPage),
                                      (r'/(.*)/(.*)', IndexPage),
                                      (r'/(.*)/', IndexPage),
                                      (r'/(.*)', IndexPage),
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

