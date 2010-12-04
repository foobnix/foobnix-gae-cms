from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from web.admin.admin import AdminPage
from web.site.view import ViewPage


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

