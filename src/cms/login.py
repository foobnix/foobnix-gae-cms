#-*- coding: utf-8 -*-
'''
Created on 7 дек. 2010

@author: ivan
'''
from google.appengine.api import users
from configuration import admins

def check_user_admin(requestHandler, user):
    if user and user.email() in admins:
        return user
    requestHandler.redirect(users.create_login_url(requestHandler.request.uri))
    return None
