#-*- coding: utf-8 -*-
'''
Created on Jan 18, 2011

@author: ivan
'''
import zlib

str = """<p class="MsoNormal"></p><p class="MsoNormal"></p><h2 style="text-align: center;"><font class="Apple-style-span" color="#006600">Приглашаем на чайную церемонию: "Пуэр - чай загадка"</font></h2><h4 style="text-align: center;">Чайная церемония у нас – это не только поглощение вкусно приготовленного чая, это вечер отличного настроения, интересных рассказов и даже … волшебства. </h4><h4 style="text-align: center;">Приходите к нам и вы узнаете: все о загадочном чае Пуэр, сможете попробовать 3 разных шу-пуэра, приготовленных различными способами: порционный пуэр, пуэр из блина и пуэр сваренный на молоке. И, что немаловажно, просто замечательно проведете вечер. </h4><h3><font class="Apple-style-span" color="#006600"><img src="http://funnyday.com.ua/wp-content/uploads/Puer-tea.jpg"></font></h3><h3><font class="Apple-style-span" color="#006600">Опытный чайный мастер поведает </font><span class="Apple-style-span" style="color: rgb(0, 102, 0); ">вам</span><span class="Apple-style-span" style="color: rgb(0, 102, 0); ">:</span></h3><p class="MsoNormal">— что же такое пуэр на самом деле (а что не пуэр);</p><p class="MsoNormal">— где кончаются сказки и байки о пуэрах и где начинается правда об этом удивительном чае;</p><p class="MsoNormal">— как отличить хороший пуэр от мягко скажем подделки (которых сейчас, к сожалению очень много);</p><p class="MsoNormal">— как правильно готовить этот чай и как извлекать из него максимум пользы, силы и даже волшебства.</p><p class="MsoNormal"><b><font class="Apple-style-span" color="#006600"><br></font></b></p><p class="MsoNormal"><b><font class="Apple-style-span" color="#006600">Место проведение чайной церемонии:</font></b> метро Контрактовая площадь, ул. Верхний Вал, дом 50, оф. 5 «Чайное место».</p><p class="MsoNormal"><b><font class="Apple-style-span" color="#006600">Время и дата: </font></b>29 января (суббота), 15.00</p><p class="MsoNormal"><b><font class="Apple-style-span" color="#006600">Длительность чайной церемонии:</font></b> 4 часа</p><p class="MsoNormal"><b><font class="Apple-style-span" color="#006600">Ведущая чайной церемонии</font></b> — чайный мастер Анастасия. Несколько лет назад она не просто увлеклась, а по-настоящему влюбилась в чай. Влюбилась настолько, что чай и проведение чайных церемоний стали не просто хобби, а самой настоящей профессией. Два года назад окончила китайскую чайную школу (все имеющиеся на сегодняшний день уровни). Немного практиковалась в японской чайной церемонии. На сегодняшний день активно занимается исследованиями и других чайных традиций: русской, индийской, тибетской. В силу накопленных знаний и практики стали рождаться собственные чайные наработки. Так, например, появились авторские программы «Чай в жизни женщины», «Пуэр — чай загадка», «Чай в истории Киева», «Чайное знание». На сегодняшний день глубоко убеждена, что чай способен сделать каждого из нас лучше — тоньше, гармоничнее, красивее — и внешне и внутренне. И все что для этого нужно — лишь искреннее желание понять душу чая.</p><h2 style="text-align: center;">С удовольствием ответим на все Ваши вопросы, звоните: </h2><h2 style="text-align: center;">097-926-48-86, 066-978-40-19 (Марина) </h2><h2 style="text-align: center;">или пишите 7funnyday7@gmail.com</h2><p class="MsoNormal" style="text-align: center;"><br></p><h4><br></h4><p class="MsoNormal"><br></p><p class="MsoNormal"><br></p><p class="MsoNormal"> </p><p></p><p></p>
"""
res = zlib.compress(str)
print res
print len(str), len(res)
print zlib.decompress(res)