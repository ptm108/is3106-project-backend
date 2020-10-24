from django.urls import path

from . import views

urlpatterns = [
  path('', views.protected_recipe_view, name='Create/Get recipes'),
  path('/<slug:pk>', views.delete_recipe, name='Delete recipe'),
  path('/undelete_recipe/<slug:pk>', views.undelete_recipe, name="undelete recipe"),
]