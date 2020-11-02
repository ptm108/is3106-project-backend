from rest_framework import serializers

from .models import Order
from groupbuys.models import Groupbuy
from recipes.serializers import RecipeSerializer
from users.serializers import DeliveryAddressSerializer, CustomUserSerializer
from groupbuys.serializers import GroupbuySerializer


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
