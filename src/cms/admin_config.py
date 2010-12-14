#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from cms.model import MenuModel, PageModel, EmailModel, ProductModel, ImageModel
positions = ["TOP", "LEFT", "No"]

LAYOUT_ONE_PAGE = "one_page"
LAYOUT_LIST_PAGE = "list_page"
LAYOUT_CATALOG_PAGE = "catalog_page"
#layouts = [LAYOUT_ONE_PAGE, LAYOUT_LIST_PAGE, LAYOUT_CATALOG_PAGE]

layouts = [{
            "id":LAYOUT_ONE_PAGE,
            "template":"one_page.html",
            "child_template":"one_page.html",
            "name":"One Page",
            "model":PageModel()
            },
            {
            "id":LAYOUT_LIST_PAGE,
            "template":"list_page.html",
            "child_template":"view_page.html",
            "name":"List Page",
            "model":PageModel()
            },
            {
            "id":LAYOUT_CATALOG_PAGE,
            "template":"catalog_page.html",
            "child_template":"view_product.html",
            "name":"Catalog Page",
            "model":ProductModel()
            },
]

IMAGE_NOT_FOUND = "/images/image-not-found.gif"

CMS_URL = "/admin"
CMS_VIEW = "CMS_VIEW"
CMS_EDIT = "CMS_EDIT"

admin_menu = [
        {
         "template_dict":"menu",
         "link_id":CMS_URL + "/menu",
         "text":"New-Edit Menu",
         "template":"admin-menu.html",
         "model":MenuModel(),
         "type":CMS_EDIT
         },
        {
         "template_dict":"page",
         "link_id":CMS_URL + "/page",
         "text":"New Page",
         "template":"admin-page.html",
         "model":PageModel(),
         "type":CMS_EDIT
         },
        {
         "template_dict":"page",
         "link_id":CMS_URL + "/pageslist",
         "text":"All Pages",
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
         },
          {
         "template_dict":"product",
         "link_id":CMS_URL + "/product",
         "text":"New Product",
         "template":"admin-product.html",
         "model":ProductModel(),
         "type":CMS_EDIT
         },
         {
         "template_dict":"image",
         "link_id":CMS_URL + "/image",
         "text":"New Image",
         "template":"admin-image.html",
         "model":ImageModel(),
         "type":CMS_EDIT
         }                     
        ]
