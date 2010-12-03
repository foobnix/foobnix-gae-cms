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
        {"id":"/admin/epages", "text":"ePages", "template":"admin-epage.html"}
        #{"id":"/admin/esettings", "text":"eSettins", "template":"admin-settings.html"}
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

def add_edit_update(handler, param1, param2, tpl, model, name, dict):
        if handler.request.get('action') == "edit":
            key_id = handler.request.get('key_id')
            menu = model.get_by_id(int(key_id))
            dict[name] = menu
                        
        if handler.request.get('action') == "addupdate":
            key_id = handler.request.get('key_id')
            if key_id:
                menu = model.get_by_id(int(key_id))
            else:
                menu = model
            add = request_to_model(menu, handler.request, name)
            add.put()
            
            handler.redirect(get_active_page(param1, param2))
            
        if handler.request.get('action') == "delete":
            key_id = handler.request.get('key_id')
            model = model.get_by_id(int(key_id))
            if model:
                model.delete()
            handler.redirect(get_active_page(param1, param2))
        
        path = os.path.join(os.path.dirname(__file__), tpl + '.html')
        return template.render(path, dict)

class AdminMenuAction():
    def __init__(self, handler, dict, param1, param2):
        self.content = add_edit_update(handler, param1, param2, "admin-emenu", MenuModel(), "menu", dict)
       
class PageAction():
    def __init__(self, dict, param1):                
            page = PageModel().all()
            page.filter("fk_menu", "/" + param1)
            page.fetch(1)
            
            path = os.path.join(os.path.dirname(__file__), 'page.html')
            if page.count() >= 1:
                self.content = template.render(path, {"page":page[0], "param1":param1})
            else:
                self.content = template.render(path, {"page":None, "param1":param1})

class AdminPageAction():
    def __init__(self, handler, dict, param1, param2):
        self.content = add_edit_update(handler, param1, param2, "admin-epages", PageModel(), "page", dict)


class AdminAction():
    def __init__(self, handler, dict, param1, param2):
        if param2 == "emenu":
            action = AdminMenuAction(handler, dict, param1, param2)            
        elif param2 == "epages":
            action = AdminPageAction(handler, dict, param1, param2)
        
        self.content = action.content
            
class EditUpateRequestHandler(webapp.RequestHandler):
    def __init__(self):
        webapp.RequestHandler.__init__(self)
    
    def get(self, param1=None, param2=None):
        dict = {
         'param1':param1,
         'param2':param2,
         'layouts':layouts,
         'positions':positions,
         'active':get_active_page(param1, param2)
         }
        
        menu_list = MenuModel().all()
        menu_list.order("-is_visible")
        menu_list.order("-position")
        menu_list.order("index")
        menu_list.fetch(50)

        dict["menu_list"] = menu_list
        
        
        page_list = PageModel().all()
        page_list.order("-is_visible")
        page_list.order("-date")
        page_list.fetch(50)
        
        dict["page_list"] = page_list
        
        content = None
        if param1 == "admin":
            content = AdminAction(self, dict, param1, param2)
        else:
            content = PageAction(dict, param1)
        
        if content:
            self.on_get(content.content, param1, param2)
        else:
            self.on_get(None, param1, param2)
        
    def on_get(self, content, param1, param2):
        pass   

class IndexPage(EditUpateRequestHandler):
    def on_get(self, content, param1, param2):
        
        menu_list = MenuModel().all()
        menu_list.order("index")
        menu_list.fetch(50)
       
        values = {
                 'menu':menu_list,
                 'admin_menu':admin_menu,
                 'param1':param1,
                 'param2':param2,
                 'active':get_active_page(param1, param2),
                 'container':content
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

