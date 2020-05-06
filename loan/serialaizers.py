from rest_framework import serializers
from django.db import transaction
from .models import LoanApplication, Borrower
from helpers.iin_helpers import get_format_birthday
from django.utils.translation import ugettext_lazy as _


class BorrowerSerializer(serializers.ModelSerializer):
    iin = serializers.CharField(max_length=12, min_length=12, label=_('IIN'))

    def validate_iin(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(_("Invalid iin format"))
        try:
            get_format_birthday(value)
        except ValueError:
            raise serializers.ValidationError(_("Invalid iin format"))
        return value

    class Meta:
        model = Borrower
        read_only_fields = ('birth_date', )
        exclude = ()


class LoanApplicationSerializer(serializers.ModelSerializer):
    borrower = BorrowerSerializer()

    @transaction.atomic()
    def create(self, validated_data):
        borrower_data = validated_data.pop('borrower')
        birth_date = get_format_birthday(borrower_data['iin'])
        borrower, created = Borrower.objects.get_or_create(
            birth_date=birth_date,
            **borrower_data)
        application = LoanApplication.objects.create(borrower=borrower, **validated_data)
        return application

    class Meta:
        model = LoanApplication
        read_only_fields = ('status', 'rejection_reason')
        exclude = ()
