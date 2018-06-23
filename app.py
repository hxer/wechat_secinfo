#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from flask import Flask
from flask.json import JSONEncoder
from flask import jsonify
from playhouse.shortcuts import model_to_dict
from models import db
from models import Paper


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):

                return obj.strftime('%y-%m-%d %H:%M')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False     # better support chinese jsonfy
app.json_encoder = CustomJSONEncoder


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.route('/')
def home():
    return 'nameless'


@app.route('/info/time')
def query_by_time():
    now = datetime.now()
    n_days = datetime(now.year, now.month, now.day) - timedelta(days=3)
    papers = Paper.select().where(Paper.post_time > n_days
                                  ).order_by(Paper.post_time.desc()
                                  ).execute()
    data = list(map(model_to_dict, papers))
    result = {
        'code': 0,
        'data': data
    }
    return jsonify(result)


@app.route('/info/hot')
def query_by_hot():
    now = datetime.now()
    n_days = datetime(now.year, now.month, now.day) - timedelta(days=3)
    papers = Paper.select().where(Paper.post_time > n_days
                                  ).order_by(Paper.read_num.desc()
                                  ).execute()
    data = list(map(model_to_dict, papers))
    remove_keys = ['author', 'content', 'wx_name', 'add_time']
    for item in data:
        for key in remove_keys:
            item.pop(key)
    result = {
        'code': 0,
        'data': data
    }
    return jsonify(result)



if __name__ == '__main__':
    app.run()
