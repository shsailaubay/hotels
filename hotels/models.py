from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _


class Hotel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Hotel name'))
    stars = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Stars count')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Hotel')
        verbose_name_plural = _('Hotels')
