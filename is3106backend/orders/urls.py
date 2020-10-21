from django.urls import path

from . import views

urlpatterns = [
  path('', views.groupbuy_view, name='search, filter, get all groupbuys'),
  path('/<slug:pk>', views.protected_groupbuy_view, name='Update/Approve Groupbuy'),
  path('/orders', views.protected_order_view, name='Create Order'),
]