import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import Address
from api.serializers import AddressSerializer

ADDRESSES_URL = "http://127.0.0.1:8000/v1/addresses/"


class GetAllAddressesTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="user1", password="12345", id=1)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.user2 = User.objects.create_user(username="user2", password="12345", id=2)

        Address.objects.create(
            owner_id=self.user.id,
            contact_name="John Doe",
            road="Road 1",
            house_number="1",
            postcode="100",
            city="City 1",
            state="State 1",
            country="Country 1",
        )
        Address.objects.create(
            owner_id=self.user.id,
            contact_name="Jane Doe",
            road="Road 2",
            house_number="2",
            postcode="200",
            city="City 2",
            state="State 2",
            country="Country 2",
        )
        Address.objects.create(
            owner_id=self.user.id,
            contact_name="Marcus Silver",
            road="Road 3",
            house_number="3",
            postcode="300",
            city="City 3",
            state="State 3",
            country="Country 3",
        )
        Address.objects.create(
            owner_id=self.user2.id,
            contact_name="Maria Gold",
            road="Road 4",
            house_number="4",
            postcode="400",
            city="City 4",
            state="State 4",
            country="Country 4",
        )

    def test_when_user_gets_all_addresses_then_only_addresses_from_user_are_returned(
            self,
    ):
        response = self.client.get(ADDRESSES_URL)

        addresses = Address.objects.filter(owner_id=self.user.id)
        serializer = AddressSerializer(addresses, many=True)

        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_when_user_is_not_authenticated_error_is_returned(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("http://127.0.0.1:8000/v1/addresses/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateNewAddressTest(APITestCase):
    """Test module for inserting a new address"""

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="12345", id=1)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.valid_payload = {
            "contact_name": "John Doe",
            "house_number": "42",
            "road": "Lake Street",
            "postcode": "ABC123",
            "city": "Los Angeles",
            "state": "California",
            "country": "United States of America"
        }

        self.invalid_payload = {
            "contact_name": "",
            "house_number": "",
            "road": "Lake Street",
            "postcode": "ABC123",
            "city": "Los Angeles",
            "state": "California",
            "country": "United States of America"
        }

    def test_create_valid_address(self):
        response = self.client.post(
            ADDRESSES_URL,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_address(self):
        response = self.client.post(
            ADDRESSES_URL,
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleAddressTest(APITestCase):
    """Test module for updating an existing address record"""

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="12345", id=1)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        john = {
            "contact_name": "John Doe",
            "house_number": "1",
            "road": "Road 1",
            "postcode": "100",
            "city": "City 1",
            "state": "State 1",
            "country": "Country 1"
        }

        response = self.client.post(ADDRESSES_URL, data=json.dumps(john), content_type="application/json")
        self.created_address_id = response.data["id"]

    def test_invalid_update_address(self):
        invalid_payload = {
            "contact_name": "",
            "house_number": "",
            "road": "New Ocean Street",
            "postcode": "ABC123",
            "city": "Los Angeles",
            "state": "California",
            "country": "United States of America"
        }

        response = self.client.put(
            ADDRESSES_URL + f"{self.created_address_id}/",
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_address(self):
        valid_payload = {
            "contact_name": "John Doe",
            "house_number": "95",
            "road": "Downtown Street",
            "postcode": "ABC999",
            "city": "San Antonio",
            "state": "California",
            "country": "United States of America"
        }

        response = self.client.put(
            ADDRESSES_URL + f"{self.created_address_id}/",
            data=json.dumps(valid_payload),
            content_type="application/json",
        )

        print("!!!!!")
        print(ADDRESSES_URL + f"{self.created_address_id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteSingleAddressTest(APITestCase):
    """ Test module for deleting an existing address record """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="12345", id=1)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        john_address = {
            "contact_name": "John Doe",
            "house_number": "1",
            "road": "Road 1",
            "postcode": "100",
            "city": "City 1",
            "state": "State 1",
            "country": "Country 1"
        }

        response = self.client.post(ADDRESSES_URL, data=json.dumps(john_address), content_type="application/json")
        self.created_address_id = response.data["id"]

    def test_valid_delete_address(self):
        response = self.client.delete(ADDRESSES_URL + f"{self.created_address_id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_address(self):
        response = self.client.delete(ADDRESSES_URL + "999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
