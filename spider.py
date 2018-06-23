#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from time import sleep
from datetime import datetime
from datetime import timedelta
from gsdata import GSException
from gsdata import GSData
from models import db
from models import Paper


def create_tables():
    with db:
        db.create_tables([Paper])


def run():
    gs = GSData()
    db.connect()

    with open('data.txt', encoding='utf-8') as f:
        for line in f:
            wx_name = line.split(' ')[0]
            try:
                data = gs.query(wx_name)
            except GSException as ex:
                print(str(ex))
                continue
            else:
                for item in data:
                    url = 'https://{0}'.format(item['url'].split('://', 1)[1])
                    md5s = hashlib.md5(url.encode('utf-8')).hexdigest()
                    if Paper.select().where(Paper.url_hash == md5s).count():
                        continue
                    print(item)
                    p = Paper.create(
                        wx_name=item['wx_name'],
                        name=item['name'],
                        title=item['title'],
                        author=item['author'],
                        content=item['content'],
                        url=url,
                        url_hash=md5s,
                        post_time=datetime.strptime(item['posttime'], '%Y-%m-%d %H:%M:%S'),
                        add_time=datetime.strptime(item['add_time'], '%Y-%m-%d %H:%M:%S')
                    )
                    if type(item['readnum_newest']) == int:
                        p.read_num = item['readnum_newest']
                    if type(item['likenum_newest']) == int:
                        p.like_num = item['likenum_newest']
                    if item['picurl']:
                        p.pic_url = item['picurl']

                    p.save()
            sleep(3)

    db.close()


if __name__ == '__main__':
    create_tables()
    run()
