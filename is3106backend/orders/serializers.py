from rest_framework import serializers

from .models import Groupbuy
from recipes.serializers import RecipeSerializer


class GroupbuySerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()
    status = serializers.CharField(source='get_status')

    class Meta:
        model = Groupbuy
        read_only_fields = (
            'status',
        )
        fields = '__all__'
    # end Meta class
# end class
