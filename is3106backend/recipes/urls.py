from django.urls import path

from . import views

urlpatterns = [
  path('', views.protected_recipe_view, name='Create/Get recipes'),
  path('/<slug:pk>', views.single_recipe_view, name='Delete recipe'),
]