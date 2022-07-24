from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Address


class AddressSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Address
        fields = [
            "id",
            "owner",
            "contact_name",
            "house_number",
            "road",
            "postcode",
            "city",
            "state",
            "country",
        ]


class UserSerializer(serializers.ModelSerializer):
    addresses = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Address.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "addresses"]
