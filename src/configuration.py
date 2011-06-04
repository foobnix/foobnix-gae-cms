#-*- coding: utf-8 -*-
'''
Created on 7 дек. 2010

@author: ivan
'''
import os
import logging

CMS_TEMPLATE = "foobnix-cms"
#CMS_TEMPLATE = "marinatext"
#CMS_TEMPLATE = "foobnix-android"


APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
#DEBUG = True
logging.info("Starting application in DEBUG mode: %s", DEBUG)


BASE_DIR = os.path.dirname(__file__)

"""template entry point"""
TEMPLATE_INDEX = os.path.join(BASE_DIR, "templates", CMS_TEMPLATE, "base.html")
TEMPLATE_PATH = os.path.dirname(TEMPLATE_INDEX)

ADMIN_TEMPLATE_INDEX = os.path.join(BASE_DIR, "administrator", "templates", "default", "base.html")
ADMIN_TEMPLATE_PATH = os.path.dirname(ADMIN_TEMPLATE_INDEX)



CMS_CFG = {
    "host":"http://" + os.environ['HTTP_HOST'],
    "version": "0.1",
    "html_type": "text/html",
    "charset": "utf-8",
    "admin-email": "ivan.ivanenko@gmail.com",
    "cache_time": 0 if DEBUG else 3600,
}

admins = ["ivan.ivanenko@gmail.com", "zavlab1@gmail.com", "ch.ceremoniya@gmail.com"]




LANG_CODE_RU = "ru"
LANG_CODE_EN = "en"
CMS_LANGUAGES = {
                 LANG_CODE_RU:"Русский",
                 LANG_CODE_EN:"English"
                 }

LANG_CODE_DEFAULT = LANG_CODE_RU           
