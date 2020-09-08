from rest_framework import serializers
from .models import Recipe, Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
    #end Meta class

# end class

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
    #end Meta class
    
# end class
