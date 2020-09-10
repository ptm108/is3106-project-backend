from rest_framework import serializers
from .models import CustomUser, DeliveryAddress


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_active', 'date_joined', 'name']
    # end class
    
# end class

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'
    # end Meta class
    
# end class
    