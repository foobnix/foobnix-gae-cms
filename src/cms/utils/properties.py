#-*- coding: utf-8 -*-
'''
Created on 21 дек. 2010

@author: ivan
'''
from cms.model import PropertieModel, MenuModel, ProductModel, PageModel
from cms.admin_config import default_properties, LAYOUT_CATALOG_PAGE, \
    LAYOUT_LIST_PAGE, LAYOUT_ONE_PAGE
from configuration import DEBUG
from cms.utils.translate import get_translated

def add_page(title, content, menu):
    page = PageModel()
    page.title_ru = title
    page.title_en = get_translated(title)
    
    page.content_ru = content
    page.content_en = get_translated(content)
    
    page.fk_menu = menu
    page.put()

def add_product(title, description, image_path, catalog_path):
    product = ProductModel()
    product.title = title
    product.description = description
    product.image_path = image_path
    product.catalog_path = catalog_path
    product.put()
    

def add_menu(id, ru, eng, pos, bg=None, layout=LAYOUT_ONE_PAGE, index=0):
    menu = MenuModel()
    menu.link_id = id
    menu.name_ru = ru
    menu.name_en = eng
    menu.position = pos
    menu.background = bg
    menu.layout = layout
    menu.index = index
    menu.put()
    

def populate_foonbix_menu():
    all = MenuModel().all()
    for item in all:
        item.delete()
        
    add_menu("welcome", "Главная", "Welcome", "TOP", None, LAYOUT_LIST_PAGE, 1)
    add_menu("about", "Описание", "Description", "TOP", None, LAYOUT_ONE_PAGE, 2)
    add_menu("screenshots", "Галерея", "Gallery", "TOP", None, LAYOUT_ONE_PAGE, 3)
    add_menu("download", "Скачать", "Download", "TOP", None, LAYOUT_ONE_PAGE, 4)
    add_menu("feedback", "Отзывы", "Feedback", "TOP", None, LAYOUT_LIST_PAGE, 5)
    add_menu("blog", "Блог", "Blog", "TOP", None, LAYOUT_LIST_PAGE, 6)
    add_menu("faq", "FAQ", "FAQ", "TOP", None, LAYOUT_LIST_PAGE, 7)
    add_menu("support", "Поддержать", "Support Us", "TOP", None, LAYOUT_LIST_PAGE, 8)
    add_menu("aboutus", "О нас", "About Us", "TOP", None, LAYOUT_ONE_PAGE, 9)
        

def populate_menu():
    all = MenuModel().all()
    for item in all:
        item.delete()
        
    add_menu("senin", "Сенин", "Senin", "TOP", "/images/bg2.jpg", LAYOUT_LIST_PAGE)
    add_menu("catalog", "Каталоr", "Catalog", "TOP", "/images/bg_l.jpg", LAYOUT_CATALOG_PAGE)
    add_menu("restavration", "Реставрация", "Restavration", "TOP", "/images/senin_51.jpg", LAYOUT_LIST_PAGE)
    add_menu("contatcs", "Контакты", "Сontacts", "TOP", "/images/bg3.jpg", LAYOUT_LIST_PAGE)
    
    all = ProductModel().all()
    for item in all:
        item.delete()
    for i in xrange(6):
        add_product("Туфли мужские", "SNMBL-703 Туфли мужские черные. Верх выполнен из натуральной кожи ската. Подкладка и подошва - из натуральной кожи.", "/images/product1/init.png", "/images/product1/")    
    
    
    all = PageModel().all()
    for item in all:
        item.delete()
    text = u"""
    «О том,что ему суждено стать обувщиком и пойти по стопам своего отца, Игорь знал с детства. Собственную мастерскую создал более десяти лет назад. За это время он собрал команду профессионалов, которые понимают друг друга с полуслова. Именно по этой причине Игорь до сих пор работает в Украине, несмотря на нелегкие условия и заманчивые предложения из-за границы».<br/><br/>
    «Изготовление пары туфель в студии Сенина длится как минимум месяц: сначала обмеривается стопа, затем изготавливается макет и лишь после этого – собственно пара обуви. Работа над моделью всегда проходит в тандеме мастера и клиента, в процессе обсуждения и общения. Мужские туфли выполняются по старинным законам обувного мастерства – подошва и корпус сшиваются льняными нитями».
    <h3>Elle, апрель 2010</h3>
    """
    add_page(u"Игорь Сенин", text, "senin")
    add_page(u"Наши контакты", u"<h2>igor.senin@gmail.com</h2> <h2>+38 067 280 77 70</h2>", "contatcs")
    text = u"""
   <h2> Реставрация обуви категории Lux</h2>

Cохранить изделия под маркой Senin, а также любую обувь класса «люкс» в первозданном виде помогает беспрецедентная услуга – реставрация обуви и аксессуаров абсолютно любой степени сложности. Индивидуальный подход и высокое качество гарантировано!

<h2>044-229-77-00</h2>

<h2>098-122-77-00</h2>

ул. Золотоворотская 2А<br/>

Время работы:<br/>

ПН-ПТ 13.00 - 19.00<br/>

СБ 11.00 - 15.00<br/>
"""
    add_page(u"", text, "restavration")
    
    
    
    
    

def populate_properties():
    if DEBUG:
        all = PropertieModel().all()
        for item in all:
            item.delete()
        
    for propertie in default_properties:        
        model = PropertieModel().all()
        model.filter("name", propertie["name"])
        
        if model.count() == 0:
            new = PropertieModel()
            new.name = propertie["name"]
            new.value_ru = propertie["value_ru"]
            new.value_en = propertie["value_en"]
            new.put()

def get_propertie(name):
    model = PropertieModel().all()
    model.filter("name", name)
    if model.count(1) == 1:
        return model.get().value_ru
    else:
        return ""
    
