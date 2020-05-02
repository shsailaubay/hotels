from rest_framework import serializers
import re
from .models import Guest

phone_pattern = re.compile("^[+][0-9-]{1,20}$")


class GuestSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        print('guest validate')
        return attrs

    def validate_phone_number(self, value):
        print('phoone validate')
        if not phone_pattern.search(value):
            raise serializers.ValidationError("Invalid phone format")
        return value

    class Meta:
        model = Guest
        exclude = ()
