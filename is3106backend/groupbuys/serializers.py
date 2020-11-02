from rest_framework import serializers

from .models import Groupbuy
from recipes.serializers import RecipeSerializer
from users.serializers import  CustomUserSerializer

class GroupbuySerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()
    status = serializers.CharField(source='get_status')
    vendor = CustomUserSerializer()

    class Meta:
        model = Groupbuy
        read_only_fields = (
            'status',
            'recipe',
            'vendor',
        )
        fields = '__all__'
    # end Meta class
# end class