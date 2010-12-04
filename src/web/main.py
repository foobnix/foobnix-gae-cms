from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

positions = ["TOP", "LEFT", "No"]
layouts = ["one_page", "list_page"]

class MenuModel(db.Model):
    link_id = db.StringProperty(multiline=False)
    name = db.StringProperty(multiline=False)
    layout = db.StringProperty(multiline=False)
    position = db.StringProperty(multiline=False)
    index = db.IntegerProperty()
    is_visible = db.BooleanProperty()
    
    def get_name(self):
        return "menu"

class PageModel(db.Model):
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    is_comment = db.BooleanProperty()
    is_visible = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    fk_menu = db.StringProperty(multiline=False)
    
    def get_name(self):
        return "page"

admin_menu = [
        {"link_id":"admin/menu", "text":"Add Menu"},
        {"link_id":"admin/page", "text":"Add Page"}
        #{"id":"/admin/esettings", "text":"eSettins", "template":"admin-settings.html"}
        ]

def prepare_glob_dict():
    menu_list = MenuModel().all()
    menu_list.order("-is_visible")
    menu_list.order("-position")
    menu_list.order("index")
    menu_list.fetch(50)
    
    page_list = PageModel().all()
    page_list.order("-is_visible")
    page_list.order("-date")
    page_list.fetch(50)
    
    glob_dict = {
     'menu_list':menu_list,
     'page_list':page_list
     }
    return glob_dict

def get_pages(menu_name):
    page = PageModel().all()
    page.filter("fk_menu", menu_name)
    return page

def get_menu_layout(menu_name):
    page = MenuModel().all()
    page.filter("link_id", menu_name)
    
    layout = layouts[0]
    
    if page.count() >= 1:
        layout = page[0].layout
        
    return layout
    

class ViewPage(webapp.RequestHandler):
    """param1 - menu name"""
    def get(self, menu_name, page_key_id=None):
        glob_dict = prepare_glob_dict()        

        if page_key_id:
            page = PageModel.get_by_id(int(page_key_id))
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
        else:
            path = os.path.join(os.path.dirname(__file__), 'admin.html')
            self.response.out.write(template.render(path, glob_dict))

application = webapp.WSGIApplication([
                                      (r'/admin/(.*)/', AdminPage),
                                      (r'/admin/(.*)', AdminPage),
                                      (r'/admin/', AdminPage),
                                      (r'/admin', AdminPage),
                                      
                                      (r'/(.*)/(.*)/', ViewPage),
                                      (r'/(.*)/(.*)', ViewPage),
                                      (r'/(.*)/', ViewPage),
                                      (r'/(.*)', ViewPage),
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

