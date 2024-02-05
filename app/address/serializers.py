from core.models import Address

from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields=['city','district','street_address','postal_code','phone_number']
    

        