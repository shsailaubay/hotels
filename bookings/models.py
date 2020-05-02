from django.db import models
from guests.models import Guest
from hotels.models import Hotel
from django.utils.translation import ugettext_lazy as _


class Booking(models.Model):
    guest = models.ForeignKey(Guest, verbose_name=_('Guest'), on_delete=models.PROTECT, related_name='bookings')
    hotel = models.ForeignKey(Hotel, verbose_name=_('Hotel'), on_delete=models.PROTECT, related_name='bookings')
    check_in_date = models.DateField(verbose_name=_('Дата заезда'))
    check_out_date = models.DateField(verbose_name=_('Дата выезда'))
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.pk)

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

