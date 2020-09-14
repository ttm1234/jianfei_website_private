import datetime
import json
import random
import time
import urllib.parse

import jwt
from flask import request
from bson import ObjectId
from hashlib import md5
from flask import Response

from config import config
import random


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def log(*args):
    # pass
    try:
        for i in args:
            print(json.dumps(i, indent=4, ensure_ascii=False, cls=JSONEncoder))
    except Exception:
        print(args)


def urlencode(str):
    return urllib.parse.quote(str)


def unix_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp


# def result_handler(data, msg='没有找到', errcode=400):
#     if data is None:
#         return {
#                    'code': errcode,
#                    'data': data,
#                    'msg': msg,
#                }, 200
#     else:
#         return {
#                    'code': 200,
#                    'data': data,
#                    'msg': 'ok',
#                }, 200


def gen_id_str(prefix=''):
    r = prefix + str(ObjectId())
    return r


def get_platform():
    r = request.headers.get('Platform')
    return r


def get_ymds():
    t0 = datetime.datetime.now()
    y = t0.strftime('%Y')
    m = t0.strftime('%Y-%m')
    d = t0.strftime('%Y-%m-%d')
    r = {
        'year': y,
        'month': m,
        'day': d,
    }
    return r


def q_all_from_q(q: dict, field: str):
    assert '__' not in field
    prefix = '{}__'.format(field)
    q_all = dict()
    for k, v in q.items():
        if not k.startswith(prefix):
            q_all[k] = v
    return q_all


def route_q_from_args_kvs(q, args, func, kvs):
    if func is bool:
        func = lambda a: False if a in ['', '0', 0, 'false', 'False'] else True

    for k_arg, k_model in kvs.items():
        a = str(args.get(k_arg) or '')
        if a:
            q[k_model] = func(a)

    return q


if __name__ == '__main__':
    pass
