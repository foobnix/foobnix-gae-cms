from google.appengine.ext import webapp
import datetime
import os
from google.appengine.ext.webapp import template
from cms.model import PageModel
class FoobnixRSS(webapp.RequestHandler):
    def get(self):    
        models = PageModel().all()
        models.order('-date')
        models.filter('fk_menu', "blog")
        models.fetch(20)
        
        lang = self.request.get('lang')
        
        template_values = {
        'lang':lang,
        'date': datetime,
        'models': models,
        }
        
        path = os.path.join(os.path.dirname(__file__), 'rss.xml')
        self.response.out.write(template.render(path, template_values))
