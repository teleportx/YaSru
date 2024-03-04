from datetime import datetime
from enum import IntEnum

from tortoise.models import Model
from tortoise import fields

from db.fields import AutoNowDatetimeField


class SretType(IntEnum):
    SRET = 1
    DRISHET = 2
    PERNUL = 3


class SretSession(Model):
    message_id = fields.BigIntField(pk=True, unique=True)
    user = fields.ForeignKeyField('models.User')

    start = AutoNowDatetimeField()
    end = fields.DatetimeField(null=True, default=None)

    autoend = fields.BooleanField(default=True)
    sret_type = fields.IntEnumField(SretType)
