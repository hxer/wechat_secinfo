#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *

from config import DATABASE


db = SqliteDatabase(DATABASE)


class Paper(Model):
    class Meta:
        database = db

    wx_name = CharField(max_length=100)
    name = CharField(max_length=100)
    title = CharField()
    author = CharField(max_length=100)
    content = TextField()
    url = CharField()
    url_hash = CharField(index=True, max_length=60)
    pic_url = CharField(null=True)
    post_time = DateTimeField(index=True)
    add_time = DateTimeField()
    read_num = IntegerField(default=0)
    like_num = IntegerField(default=0)
