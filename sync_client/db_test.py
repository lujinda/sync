#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 20:10:00
# Filename        : db_test.py
# Description     : 

from pymongo import Connection
from db import DB

db = DB(Connection().test)
print(db.test.insert_sync({'no': 1}))

