from django.urls import path

from . import views

urlpatterns = [
  path('', views.DefaultView.as_view(), name='default'),
  path('all_groupbuys', views.all_groupbuys, name='search, filter, get all groupbuys'),
  path('approve_groupbuy/<slug:pk>', views.approve_groupbuy, name='Approve groupbuy'),
  path('update_groupbuy/<slug:pk>', views.update_groupbuy, name='Update group buy (Vendor)'),
  path('create_order', views.create_order, name='create new order'),
]