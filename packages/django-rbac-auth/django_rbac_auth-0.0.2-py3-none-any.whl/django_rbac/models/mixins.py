from django.db import models


class RecursionMixin(models.Model):
    parent = models.ForeignKey(verbose_name='parent', to='self', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        abstract = True
