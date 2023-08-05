from django.db import models
from .base import BaseModel
from .user import User
from .role import Role
from .permission import Permission
from .mixins import RecursionMixin


class Group(BaseModel, RecursionMixin):
    users = models.ManyToManyField(verbose_name='users', to=User)
    roles = models.ManyToManyField(verbose_name='roles', to=Role)
    permissions = models.ManyToManyField(verbose_name='permissions', to=Permission)

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = verbose_name
