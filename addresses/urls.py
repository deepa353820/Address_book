# addresses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddressListCreateView.as_view(), name='address-list-create'),
    path('<int:pk>/', views.AddressRetrieveUpdateDestroyView.as_view(), name='address-detail'),
    path('nearby/', views.NearbyAddressView.as_view(), name='address-nearby'),
]
