from .base import BaseModel
from .permission import Permission
from .mixins import RecursionMixin
from django.db import models


class Role(BaseModel, RecursionMixin):
    permissions = models.ManyToManyField(verbose_name='permissions', to=Permission)

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = verbose_name
