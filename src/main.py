#-*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging

from cms.view import SendEmails, ViewPage
from cms.admin import ViewImage, AdminPage
import os
from configuration import DEBUG
import sys
from cms.utils.properties import populate_properties
from cms.utils.twitter import TwitterTagCrawler
from cms.statistics import SubmitVersion

#sys.path.insert(0, APP_ROOT_DIR)
#sys.path.insert(1, os.path.join(APP_ROOT_DIR, TEMPLATE_PATH))

if not DEBUG:
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    except Exception, e:
        logging.error(e)


logging.getLogger().setLevel(logging.DEBUG)

webapp.template.register_template_library('cms.filter.text_filter')
webapp.template.register_template_library('cms.tag')

logging.info('Loading %s, app version = %s',
             __name__, os.getenv('CURRENT_VERSION_ID'))

populate_properties()


class Twits(webapp.RequestHandler):
    def get(self):
        self.response.out.write("<br>begin<br>")        
        self.response.out.write(TwitterTagCrawler("foobnix", None, None).search())
        self.response.out.write("<br>eng<br>")

ROUTES = [
  
  ('/twits', Twits),
  ('/version', SubmitVersion),
  
  (r'/send_emails/(.*)', SendEmails),
  
  (r'/img/(.*)/(.*)', ViewImage),
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

application = webapp.WSGIApplication(ROUTES, debug=DEBUG)



def main():
    
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

