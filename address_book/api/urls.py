from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api import views

urlpatterns = [
    path("v1/addresses/", views.AddressList.as_view()),
    path("v1/addresses/<int:pk>/", views.AddressDetail.as_view()),
    path("v1/users/", views.UserList.as_view()),
    path("v1/users/<int:pk>", views.UserDetail.as_view()),
    path("v1/auth/login/", obtain_auth_token),
    path("v1/auth/logout/", views.Logout.as_view()),
]
