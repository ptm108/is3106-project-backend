from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import CustomUser, DeliveryAddress
from .serializers import CustomUserSerializer, DeliveryAddressSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    # end def
# end class

@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    """
    Creates a new application user
    """

    if request.method == 'POST':
        content = {"message": "Successfully created"}
        data = request.data  # {'email': 'd@d.com', 'password': 'password2'}

        try:
            user = CustomUser(email=data['email'], password=data['password'])
            user.save()

            return Response(content, status=status.HTTP_201_CREATED)
        except ValueError:
            content.message = 'Invalid data'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        # end try-except

    # end if

    return Response({}, status=status.HTTP_400_BAD_REQUEST)

# end def

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Marks user as deleted when called
    """

    if request.method == 'DELETE':
        content = {'message': 'Successfully deleted'}

        try:
            user = CustomUser.objects.get(email=request.user)

            # setting is_active to False -> marked as deleted
            user.is_active = False
            user.save()

            return Response(content, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExists:
            content.message = 'Unsuccessful'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        # end try-except

    # end if

# end def

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_delivery_address(request):
    """
    Creates a new delivery address
    """

    if request.method == 'POST':
        user = request.user
        data = request.data 

        with transaction.atomic():
            deliveryAddress = DeliveryAddress(
                address_line1 = data['address_line1'], 
                address_line2 = data['address_line2'], 
                postal_code = data['postal_code'], 
                user=user
            )
            deliveryAddress.save()
        # end with
        return Response({'message': 'Delivery Address created'}, status=status.HTTP_200_OK)
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)

# end def

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_delivery_address(request, pk):
    '''
    Deletes a delivery address
    '''
    if request.method == 'DELETE':
        user = request.user
        try:  
            DeliveryAddress.deliveryAddress_list.filter(user=user, pk=pk).delete()
            return Response({'message': 'Delivery address deleted'}, status=status.HTTP_200_OK)
        except DeliveryAddress.DoesNotExist:
            return Response({'message': 'Recipe not found'}, status=status.HTTP_200_OK)
        # end try-except
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_delivery_addresses(request):
    '''
    Retrieves all delivery addresses created by user making request
    '''
    if request.method == 'GET':
        user = request.user
        try:
            deliveryAddresses = DeliveryAddress.deliveryAddress_list.filter(user=user)
            serializer = DeliveryAddressSerializer(deliveryAddresses, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except DeliveryAddress.DoesNotExist:
            return Response({'message': 'No delivery address found'}, status=status.HTTP_200_OK)
        # end try-except

    # end if

    # return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)

# end def
