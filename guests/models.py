from django.db import models
from django.utils.translation import ugettext_lazy as _


class Guest(models.Model):
    last_name = models.CharField(max_length=255, verbose_name=_('Last Name'))
    first_name = models.CharField(max_length=255, verbose_name=_('First name'))
    birth_date = models.DateField(verbose_name=_('Date of birth'))
    phone_number = models.CharField(max_length=25, verbose_name=_('Phone number'))

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)

    class Meta:
        verbose_name = _('Guest')
        verbose_name_plural = _('Guests')
        ordering = ['last_name', 'first_name']

