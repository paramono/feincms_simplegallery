from django.db import models
from django.utils.translation import ugettext_lazy as _


class OrderableMixin(models.Model):
    _order = models.IntegerField(_('Order'), default=0)

    class Meta:
        abstract = True
