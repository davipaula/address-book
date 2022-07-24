from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from api.custom_pagination import CustomPagination
from api.filters import AddressFilter
from api.models import Address
from api.serializers import AddressSerializer


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressList(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AddressFilter
