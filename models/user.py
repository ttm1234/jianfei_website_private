from mongoorm import fields, DocModel, Meta
import json

from utils import gen_id_str, unix_timestamp


class User(DocModel):

    _id = fields.String(nullabled=False)
    qq = fields.String(nullabled=False)
    nickname = fields.String(nullabled=False)
    password = fields.String(nullabled=False)

    ct = fields.Integer()
    ut = fields.Integer()
    deleted = fields.Boolean(default=False, nullabled=False)

    meta = Meta(
        db_alias='db-jianfei',
        collection='user',
    )

    @property
    def id(self):
        return self._id

    @classmethod
    def one_from_qq(cls, qq):
        m = cls.filter_one_by(deleted=False, qq=qq)
        return m

    @classmethod
    def get_one(cls, user_id):
        m = cls.filter_one_by(deleted=False, _id=user_id)
        return m

    def valid_password(self, password):
        return self.password == password

