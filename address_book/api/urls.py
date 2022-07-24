from django.urls import path

from api import views

urlpatterns = [
    path('v1/addresses/', views.AddressList.as_view()),
    path('v1/addresses/<int:pk>/', views.AddressDetail.as_view()),
]
