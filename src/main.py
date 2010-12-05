from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from web.admin.admin import AdminPage, ViewImage
from web.site.view import ViewPage
#logging.getLogger().setLevel(logging.DEBUG)

webapp.template.register_template_library('filter.text_filter')

ROUTES = [
  (r'/img/(.*)/', ViewImage),
  (r'/img/(.*)', ViewImage),
  (r'/admin/(.*)/', AdminPage),
  (r'/admin/(.*)', AdminPage),
  (r'/admin/', AdminPage),
  (r'/admin', AdminPage),
  (r'/(.*)/(.*)/', ViewPage),
  (r'/(.*)/(.*)', ViewPage),
  (r'/(.*)/', ViewPage),
  (r'/(.*)', ViewPage)
  ]   

application = webapp.WSGIApplication(ROUTES, debug=True)

def main():
    
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

