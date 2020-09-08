from django.contrib import admin
from .models import Recipe, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_id', 'recipe_name', 'owner', 'fulfillment_date' , 'final_price')
# end class

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('ing_id', 'foreign_id', 'ing_name', 'category')
# end class

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
