from rest_framework import serializers

from api.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "contact_name", "house_number", "road", "postcode", "city", "state", "country"]
