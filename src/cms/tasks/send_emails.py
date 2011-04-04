#-*- coding: utf-8 -*-
'''
Created on Jan 18, 2011

@author: ivan
'''
import logging
import re
from cms.model import EmailModel, ImageModel, EmailStatisticModel
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.api.labs.taskqueue import taskqueue

def send_email(sender, to, subject, body):
    mail.send_mail(sender=sender,
              to=to,
              subject=subject,
              body=body)

class MailWorker(webapp.RequestHandler):
    def post(self):
        try:
            self.inline()
        except Exception, e :
            logging.error(e)
        return True
        
    def inline(self):
        count = self.request.get('count')
        to = self.request.get('to')
        id = self.request.get('id')
        
        email = EmailModel().get_by_id(int(id))        
        attachment = email.attachments
        
        attachments = []
        if attachment:
            list = attachment.split(",")
            for id in list:
                image = ImageModel.get_by_id(int(id))
                if image:
                    attachments.append((image.title + ".png", image.content))
        
        params = dict(sender=email.send_from,
                       to=to,
                       subject=email.subject,
                       body=email.message,
                       html=email.message
                       )
        
        if attachments:
            params['attachment'] = attachments
        
        statistic = EmailStatisticModel()
        statistic.count = int(count)
        statistic.send_to = to
        statistic.subject = email.subject
                      
        try:  
            mail.send_mail(**params)
            statistic.status = "OK"
        except Exception, e:
            logging.error(e)
            statistic.status = "Fail %s from: %s to: %s" % (str(e), email.send_from, to)
            
        statistic.put()
        logging.debug("send OK %s" % to)
        return True

class SendEmails(webapp.RequestHandler):
    def get(self, key_id):
        
        key_id = int(key_id)
        email = EmailModel().get_by_id(key_id)
        count = 0
        for to in re.split("[ ,;:\n\r]", email.send_to):
            if to and is_valid_email(to):
                count += 1
                try:
                    
                    
                    
                    
                    taskqueue.add(url='/mail_worker', params=dict(count=count, id=key_id, to=to))
                except Exception, e:
                    email.statistic = str(e)
                    email.status = "Erorr"
                    email.put()
                    self.redirect("admin/email?action=edit&email.key_id=%s" % key_id)
                    return None
        
        email.status = "In process"  
        email.put()
        self.redirect("/admin/email_statistic")
        return True
   
    
def is_valid_email(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False

