from rest_framework import serializers
from .models import Recipe, Ingredient

from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
    # end Meta class

# end class


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    photo_url = serializers.SerializerMethodField('get_recipe_photo')
    owner = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields = (
            'recipe_id',
            'recipe_name',
            'date_created',
            'estimated_price_start',
            'estimated_price_end',
            'deleted',
            'owner',
            'photo_url',
            'ingredients',
        )
    # end Meta class

    def get_recipe_photo(self, obj):
        request = self.context.get("request")
        if obj.display_photo and hasattr(obj.display_photo, 'url'):
            return request.build_absolute_uri(obj.display_photo.url)
        else:
            return request.build_absolute_uri('/static/recipe.jpg')
        # end if-else
    # end def

# end class
