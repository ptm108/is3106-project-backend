from rest_framework import serializers

from .models import Groupbuy, Order
from recipes.serializers import RecipeSerializer
from users.serializers import DeliveryAddressSerializer, CustomUserSerializer


class GroupbuySerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()
    status = serializers.CharField(source='get_status')
    vendor = CustomUserSerializer()

    class Meta:
        model = Groupbuy
        read_only_fields = (
            'status',
            'recipe',
            'vender',
        )
        fields = '__all__'
    # end Meta class
# end class

class OrderSerializer(serializers.ModelSerializer):
    groupbuy = GroupbuySerializer()
    delivery_address = DeliveryAddressSerializer()

    class Meta:
        model = Order
        read_only_fields = (
            'groupbuy',
            'delivery_address',
        )
        fields = '__all__'
    # end Meta class
# end class
