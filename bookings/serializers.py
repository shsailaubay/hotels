from rest_framework import serializers
from datetime import date
from .models import Booking
from guests.models import Guest
from guests.serializers import GuestSerializer
from django.db import transaction


class BookingSerializer(serializers.ModelSerializer):
    """
    Не сделал метод для редактирования
    """
    guest = GuestSerializer()

    @transaction.atomic()
    def create(self, validated_data):
        guest_date = validated_data.pop('guest')
        guest = Guest.objects.create(**guest_date)
        booking = Booking.objects.create(guest=guest, **validated_data)
        return booking

    def validate(self, attrs):
        if attrs['check_in_date'] > attrs['check_out_date']:
            raise serializers.ValidationError("Check-out date must be greater than check-in date")
        return attrs

    def validate_check_in_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Check-in date must be greater than today")
        return value

    class Meta:
        model = Booking
        exclude = ()
