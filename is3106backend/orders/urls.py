from django.urls import path

from . import views

urlpatterns = [
  path('', views.DefaultView.as_view(), name='default'),
  path('all_groupbuys', views.all_groupbuys, name="get all groupbuys"),
]