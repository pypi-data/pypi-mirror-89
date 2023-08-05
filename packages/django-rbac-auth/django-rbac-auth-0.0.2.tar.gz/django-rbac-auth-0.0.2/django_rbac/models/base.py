from django.db import models


class _Manager(models.Manager):
    def get_queryset(self):
        return super(_Manager, self).get_queryset().filter(isdelete=False)


class BaseModel(models.Model):
    objects = _Manager()
    is_delete = models.BooleanField(verbose_name='is deleted', default=False)
    order = models.PositiveIntegerField(verbose_name='order, the bigger, the farther forward')
    create_time = models.DateTimeField(verbose_name='create time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='update time', auto_now=True)

    class Meta:
        abstract = True
