from random import randint

from tortoise import fields
from tortoise.models import Model

from db.fields import AutoNowDatetimeField


class Group(Model):
    @staticmethod
    def generate_password() -> int:
        return randint(100000, 999999)

    name = fields.CharField(max_length=32)
    owner = fields.ForeignKeyField('models.User', related_name='groups_owned')

    members = fields.ManyToManyField('models.User', related_name='groups_member')
    requests = fields.ManyToManyField('models.User', related_name='groups_requested')

    notify_perdish = fields.BooleanField(default=True)
    password = fields.IntField(default=generate_password)

    created_at = AutoNowDatetimeField()
