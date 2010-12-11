
from google.appengine.ext import webapp
import os
from cms.admin_config import IMAGE_NOT_FOUND
from cms.glob_dict import prepare_glob_dict
from cms.localization18n import Resources
from configuration import CMS_CFG
register = webapp.template.create_template_register()
from google.appengine.ext.webapp import template

@register.simple_tag
def img_preview(item):
    path = os.path.join(os.path.dirname(__file__), "img_preview.html")
    return template.render(path, {"item":item})  

@register.simple_tag
def image_not_found():
    return IMAGE_NOT_FOUND

@register.simple_tag
def all_img_preview(count=None):    
    list = prepare_glob_dict()["image_list"]    
    path = os.path.join(os.path.dirname(__file__), "all_img_preview.html")
    if count:
        return template.render(path, {"image_list":list[:int(count)], "cfg":CMS_CFG})
    else:
        return template.render(path, {"image_list":list, "cfg":CMS_CFG})  


@register.simple_tag
def img_preview_from_list(list_ids):
    result = []
    if list_ids:    
        list = prepare_glob_dict()["image_list"]
        for item in list:
            if str(item.key().id()) in list_ids:
                result.append(item)
            
    path = os.path.join(os.path.dirname(__file__), "all_img_preview.html")    
    return template.render(path, {"image_list":result})  


@register.simple_tag
def text(param):
    res = Resources()
    return res.get(param)
    
