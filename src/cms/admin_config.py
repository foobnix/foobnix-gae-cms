#-*- coding: utf-8 -*-
'''
Created on 4 дек. 2010

@author: ivan
'''
from cms.model import MenuModel, PageModel, EmailModel, ProductModel, ImageModel, \
    PropertieModel, CommentModel, StatisticModel
from cms.utils.translate import get_translated
positions = ["TOP", "BLOCK", "FOOTER", "ADDITIONAL", "No"]

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
         "template_dict":"propertie",
         "link_id":CMS_URL + "/propertie",
         "text":"New Propertie",
         "template":"admin-propertie.html",
         "model":PropertieModel(),
         "type":CMS_EDIT
         },
         {
         "template_dict":"comment",
         "link_id":CMS_URL + "/comment",
         "text":"New Comment",
         "template":"admin-comment.html",
         "model":CommentModel(),
         "type":CMS_EDIT
         },
         {
         "template_dict":"statistic",
         "link_id":CMS_URL + "/statistic",
         "text":"View Statistics",
         "template":"admin-statistic.html",
         "model":StatisticModel(),
         "type":CMS_EDIT
         },
         {
         "template_dict":"email_statistic",
         "link_id":CMS_URL + "/email_statistic",
         "text":"Email Statistics",
         "template":"admin-email-statistic.html",
         "model":StatisticModel(),
         "type":CMS_EDIT
         }
        ]

footer = u"""
<p>Foobnix бесплатный плеер для Linux. Автор Иван Иваненко. 2010-2011 <a href="mailto:ivan.ivanenko@gmail.com"> ivan.ivanenko@gmail.com</a><br/>
              Сайт работает на движке <a href="https://github.com/foobnix/foobnix-gae-cms">foobnix-gae-cms</a></p>
"""


def p(name, value1, value2):
    return {"name":name, "value_ru":value1, "value_en":value2}
default_properties = [
p("foobnix.header.slogan", "Foobnix простой и мощный плеер музыки для Linux", "Foobnix simple and powerful music player for Linux"),
p("foobnix.title.slogan", "Хороший плеер для музыки и видео", "Good music and video player"),
p("foobnix.footer.text", footer, get_translated(footer)),
p("prop.wrong.text", "Неправильный текст", "Wrong Text"),
p("prop.blog", "Блог", "Blog"),
p("prop.comments", "Комментарии", "Comments"),
p("prop.comment", "Комментарий", "Comment"),
p("prop.twitter", "Твиттер", "Twitter"),
p("prop.add.new.comment", "Добавить комментарий", "Add new comment"),
p("prop.add", "Добавить", "Add"),
p("prop.delete", "Удалить", "Delete"),
p("prop.required", "Обязательное", "Required"),
p("prop.wrong.text", "Неправильный текст", "Wrong Text"),
p("prop.name", "Имя", "Name"),
p("prop.site", "Сайт", "Site"),
p("config.blog.section", "blog", "blog"),
p("config.version", "0.2.2-10", "0.2.2-10"),




]
