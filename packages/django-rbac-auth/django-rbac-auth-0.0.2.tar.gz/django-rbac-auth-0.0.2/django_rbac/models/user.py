from django.db import models
from .base import BaseModel
from .role import Role
from .permission import Permission


class User(BaseModel):
    permissions = models.ManyToManyField(verbose_name='permissions', to=Permission)
    roles = models.ManyToManyField(verbose_name='roles', to=Role)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = verbose_name
