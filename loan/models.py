from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _


class BlackList(models.Model):
    iin = models.CharField(max_length=12, unique=True, db_index=True,
                           validators=[MinLengthValidator(12)], verbose_name=_('IIN'))

    def __str__(self):
        return self.iin

    class Meta:
        verbose_name = _('Black list')
        verbose_name_plural = _('Black list')


class Borrower(models.Model):
    iin = models.CharField(max_length=12, unique=True, db_index=True,
                           validators=[MinLengthValidator(12)], verbose_name=_('IIN'))
    birth_date = models.DateField(verbose_name=_('Date of birth'), null=True)

    def __str__(self):
        return self.iin

    class Meta:
        verbose_name = _('The Borrower')
        verbose_name_plural = _('Borrowers')


class LoanProgram(models.Model):

    def save(self, *args, **kwargs):
        self.pk = 1
        super(LoanProgram, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    min_sum = models.PositiveIntegerField(default=0, verbose_name=_('Minimum loan amount'))
    max_sum = models.PositiveIntegerField(default=0, verbose_name=_('Maximum loan amount'))
    min_age = models.PositiveSmallIntegerField(default=0, verbose_name=_('Minimum age'))
    max_age = models.PositiveSmallIntegerField(default=0, verbose_name=_('Maximum age'))

    def __str__(self):
        return '{} - {} / {} - {}'.format(self.min_sum, self.max_sum, self.min_age, self.max_age)

    class Meta:
        verbose_name = _('Loan program')
        verbose_name_plural = _('Loan programs')
        # unique_together = ['min_sum', 'max_sum', 'min_age', 'max_age']


class LoanApplication(models.Model):
    CREATED = 'CR'
    ACCEPTED = 'AC'
    REJECTED = 'RE'

    STATUS_CHOICES = (
        (CREATED, _('Created')),
        (ACCEPTED, _('Accepted')),
        (REJECTED, _('Rejected'))
    )

    borrower = models.ForeignKey(Borrower, on_delete=models.PROTECT,
                                 verbose_name=_('The borrower'), related_name='applications')
    amount = models.PositiveIntegerField(verbose_name=_('Loan amount'))
    status = models.CharField(max_length=2, verbose_name=_('Status'), choices=STATUS_CHOICES, default=CREATED)
    rejection_reason = models.CharField(blank=True, default='', verbose_name=_('Rejection reason'), max_length=255)

    def __str__(self):
        return "{} / amount {}".format(self.borrower_id, self.amount)

    class Meta:
        verbose_name = _('Loan application')
        verbose_name_plural = _('Loan applications')


