from django.contrib import admin
from .models import Recipe, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_id', 'recipe_name', 'owner', 'final_price', 'fulfillment_date')
# end class

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('ing_id', 'foreign_id', 'ing_name', 'category', 'recipe')
# end class

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
