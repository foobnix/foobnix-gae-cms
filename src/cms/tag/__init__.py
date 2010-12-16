
from google.appengine.ext import webapp
import os
from cms.admin_config import IMAGE_NOT_FOUND
from cms.glob_dict import prepare_glob_dict
from configuration import CMS_CFG, CMS_LANGUAGES, LANG_CODE_RU, \
    LANG_CODE_DEFAULT
from cms.model import PropertieModel
register = webapp.template.create_template_register()
from google.appengine.ext.webapp import template

@register.simple_tag
def lang_name(lang_code):
    if lang_code and CMS_LANGUAGES.has_key(lang_code):
        return CMS_LANGUAGES[lang_code]
    else:
        return CMS_LANGUAGES[LANG_CODE_RU]

@register.simple_tag
def img_preview(item):
    path = os.path.join(os.path.dirname(__file__), "img_preview.html")
    return template.render(path, {"item":item})  

@register.simple_tag
def change_langs(model, lang, id=None):
    path = os.path.join(os.path.dirname(__file__), "lang.html")
    return template.render(path, {"langs": CMS_LANGUAGES, "lang":lang, "id":id, "model":model})  

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
def get_attr(object, param, lang=LANG_CODE_DEFAULT):
    if lang not in CMS_LANGUAGES.keys():       
        lang = LANG_CODE_DEFAULT
    
    if not object:
        return ""
    return getattr(object, param + lang)

@register.simple_tag
def get_propertie(name_key, lang=LANG_CODE_DEFAULT):
    if lang not in CMS_LANGUAGES.keys():       
        lang = LANG_CODE_DEFAULT
        
    result = "[%s.%s]" % (name_key, lang)
    
    if lang in CMS_LANGUAGES.keys():         
        properties = PropertieModel().all()
        properties.filter("name", name_key)
        
        if properties.count() > 0:
            result = getattr(properties[0], "value_" + lang)
            
    return result

