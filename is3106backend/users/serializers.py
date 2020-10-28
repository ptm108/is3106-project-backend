from rest_framework import serializers
from .models import CustomUser, DeliveryAddress, VendorUser


class CustomUserSerializer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField('get_profile_photo_url')
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'is_active', 'date_joined', 'name', 'contact_number', 'profile_photo_url',)
    # end Meta 

    def get_profile_photo_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.profile_photo.url)
    # end def
    
# end class

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'
    # end Meta class
    
# end class

class VendorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = VendorUser
        fields = '__all__'
    # end Meta class

# end class
    