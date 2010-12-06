
from google.appengine.ext import webapp
import os
from web.glob_dict import prepare_glob_dict
from web.config import IMAGE_NOT_FOUND
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
        return template.render(path, {"image_list":list[:int(count)]})
    else:
        return template.render(path, {"image_list":list})  


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
