from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.custom_pagination import CustomPagination
from api.filters import AddressFilter, IsOwnerFilterBackend
from api.models import Address
from api.permissions import IsOwnerOrReadOnly
from api.serializers import AddressSerializer, UserSerializer


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class AddressList(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    pagination_class = CustomPagination
    filter_backends = [IsOwnerFilterBackend]
    filterset_class = AddressFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)

        return Response("User logged out successfully")
