#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from web.model import MenuModel, PageModel, EmailModel

positions = ["TOP", "LEFT", "No"]
layouts = ["one_page", "list_page"]

CMS_URL = "/admin"
CMS_VIEW = "CMS_VIEW"
CMS_EDIT = "CMS_EDIT"

admin_menu = [
        {
         "template_dict":"menu",
         "link_id":CMS_URL + "/menu",
         "text":"Add Menu",
         "template":"admin-menu.html",
         "model":MenuModel(),
         "type":CMS_EDIT
         },
        {
         "template_dict":"page",
         "link_id":CMS_URL + "/page",
         "text":"Add Page",
         "template":"admin-page.html",
         "model":PageModel(),
         "type":CMS_EDIT
         },
        {
         "template_dict":"page",
         "link_id":CMS_URL + "/pageslist",
         "text":"Pages List",
         "template":"admin-pageslist.html",
         "model":PageModel(),
         "type":CMS_EDIT
         },
        {
         "template_dict":"email",
         "link_id":CMS_URL + "/email",
         "text":"Send Email",
         "template":"admin-email.html",
         "model":EmailModel(),
         "type":CMS_EDIT
         }        
        ]
