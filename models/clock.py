from mongoorm import fields, DocModel, Meta
import json
from datetime import datetime

from utils import gen_id_str, unix_timestamp


class Clock(DocModel):

    _id = fields.String(nullabled=False)
    user_id = fields.String(nullabled=False)
    user_nick = fields.String(nullabled=False)
    weight = fields.Float(nullabled=False)
    msg = fields.String(nullabled=False)
    ct_str = fields.String(nullabled=False)

    ct = fields.Integer(required=False, default=unix_timestamp)
    ut = fields.Integer(required=False, default=unix_timestamp)
    deleted = fields.Boolean(default=False, nullabled=False)

    meta = Meta(
        db_alias='db-jianfei',
        collection='clock',
    )

    @property
    def id(self):
        return self._id

    @property
    def weight_str(self):
        # todo format number 不熟
        n = self.weight
        s = '%.2f' % n
        if len(s) < 5:
            s = '0' * (5 - len(s)) + s
        # print(f'--{s}--')
        return s

    @classmethod
    def new(cls, user, data):
        t = unix_timestamp()

        m = cls()
        m._id = gen_id_str()
        m.user_id = user.id
        m.user_nick = user.nickname
        m.weight = float(data['weight'])
        m.msg = str(data['msg'])

        m.ct_str = datetime.fromtimestamp(t / 1000).strftime("%Y-%m-%d %H:%M:%S")

        m.ct = t
        m.ut = t
        m.deleted = False

        m.save()
        return m

    @classmethod
    def paging(cls, q, offset=0, limit=-1, order_by='-ct'):
        if order_by.startswith('-'):
            order_by = order_by[1:]
            fangxiang = -1
        else:
            fangxiang = 1

        if 'deleted' not in q:
            q['deleted'] = False
        ms = cls.filter_by(**q).sort(order_by, fangxiang)
        count = ms.count()
        if limit > 0:
            ms = ms.skip(offset).limit(limit)
        else:
            ms = ms.skip(offset)
        return ms, count


