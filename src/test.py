#-*- coding: utf-8 -*-
'''
Created on 14 дек. 2010

@author: ivan
'''
from cms.model import StatisticModel

find = StatisticModel().all()
print find.count()
for line in find:
    print find.userUUID
