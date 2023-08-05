from .base import BaseModel
from .mixins import RecursionMixin
from django.db import models
import abc


class Permission(BaseModel, RecursionMixin):
    name = models.CharField(verbose_name='name', max_length=255)
    description = models.CharField(verbose_name='description', max_length=500)

    class Meta:
        verbose_name = 'permission'
        verbose_name_plural = verbose_name


class AbstractConrtoller(BaseModel):
    permission = models.ForeignKey(verbose_name='permission', to=Permission, on_delete=models.CASCADE)

    @abc.abstractmethod
    def controller(self, *args, **kwargs):
        pass

    class Meta:
        abstract = True


class RouteController(AbstractConrtoller, models.Model):
    route = models.CharField(verbose_name='route', max_length=255)

    def controller(self, *args, **kwargs):
        print('===== 校验路由权限 =====')

    class Meta:
        verbose_name = 'route controller'
        verbose_name_plural = verbose_name
