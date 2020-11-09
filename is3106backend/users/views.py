from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .models import CustomUser, VendorUser, DeliveryAddress
from .serializers import CustomUserSerializer, DeliveryAddressSerializer, VendorSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    # end def
# end class


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_view(request):
    """
    Creates a new application user
    """

    if request.method == 'POST':
        content = {"message": "Successfully created"}
        data = request.data  # {'email': 'd@d.com', 'password': 'password2'}

        with transaction.atomic():
            try:
                user = CustomUser.objects.create_user(data['email'], data['password'])
                if 'name' in data and data['name'] is not None:
                    user.name = data['name']
                # end if

                user.save()

                if 'vendor_name' in data:
                    vendor = VendorUser(user=user, vendor_name=data['vendor_name'], is_vendor=True)
                    vendor.save()
                # end if
            except IntegrityError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except

            return Response(content, status=status.HTTP_201_CREATED)
        # end with
    # end if
    return Response(status=status.HTTP_400_BAD_REQUEST)

# end def


@api_view(['GET', 'DELETE', 'PATCH', 'PUT'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@parser_classes((MultiPartParser, FormParser, JSONParser))
def protected_user_view(request, pk):
    '''
    Get current user
    '''
    if request.method == 'GET':

        try:
            user = CustomUser.objects.get(pk=pk)

            if hasattr(VendorUser.objects.get(user=user), 'is_vendor'):
                vendor = VendorUser.objects.get(user=user)
                serializer = VendorSerializer(vendor, context={"request": request})
            
                return Response(serializer.data, status=status.HTTP_200_OK)
            # end if
            
        except VendorUser.DoesNotExist:
            serializer = CustomUserSerializer(user, context={"request": request})
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

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

        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except

    # end if

    """
    Updates user profile
    """

    if request.method == 'PUT':
        data = request.data

        try:
            user = CustomUser.objects.get(pk=pk)

            # checks if requesting user is same user
            if (user != request.user): return Response(status=status.HTTP_401_UNAUTHORIZED)

            if 'name' in data:
                user.name = data['name']
            if 'contact_number' in data:
                user.contact_number = data['contact_number']
            if 'profile_photo' in data:
                user.profile_photo = data['profile_photo']
            # end ifs

            user.save()

            if 'vendor_name' in data:
                try:
                    vendor = VendorUser.objects.get(user=user)
                    vendor.vendor_name = data['vendor_name']
                    vendor.save()
                except VendorUser.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                # end try-except
            # end if

            return Response(status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        # end try-except

    # end if

    """
    Change user password
    """
    if request.method == 'PATCH':
        data = request.data
        try:
            old_password, new_password1, new_password2 = data['old_password'], data['new_password1'], data['new_password2']
        except (ValueError, KeyError):
            return Response({'message': 'Check your data'}, status=status.HTTP_400_BAD_REQUEST)

        # end try-except

        try:
            user = CustomUser.objects.get(pk=pk)

            # checks if requesting user is same user
            if (user != request.user): return Response(status=status.HTTP_401_UNAUTHORIZED)

            currentpassword = user.password  # user's current password
            matchcheck = check_password(old_password, currentpassword)

            if matchcheck:
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                else:
                    return Response({'message': 'new password does not match retype password'}, status=status.HTTP_400_BAD_REQUEST)

                # end if else statement make sure new and retype password is the same

                return Response({'message': 'password updated'}, status=status.HTTP_200_OK)

            # end if statement to check if encoded password is the same as user inputted password

            return Response({'message': 'check values'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        # end try-except

    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)

# end def


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def protected_user_delivery_address_view(request, pk):
    """
    Creates a new delivery address
    """

    if request.method == 'POST':
        user = request.user
        data = request.data

        with transaction.atomic():
            try:
                deliveryAddress = DeliveryAddress(
                    address_line1=data['address_line1'],
                    address_line2=data['address_line2'] if 'address_line2' in data else None,
                    postal_code=data['postal_code'],
                    user=user
                )
                deliveryAddress.save()
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # end try-except
        # end with
        return Response({'message': 'Delivery Address created', 'add_id': deliveryAddress.add_id}, status=status.HTTP_200_OK)
    # end if

    '''
    Retrieves all delivery addresses created by user making request
    '''
    if request.method == 'GET':
        user = request.user
        try:
            deliveryAddresses = DeliveryAddress.address_list.filter(user=user)
            serializer = DeliveryAddressSerializer(deliveryAddresses, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except DeliveryAddress.DoesNotExist:
            return Response({'message': 'No delivery address found'}, status=status.HTTP_200_OK)
        # end try-except

    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)

# end def


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def protected_user_delivery_address_delete_view(request, pk, da_id):
    '''
    Deletes a delivery address
    '''
    if request.method == 'DELETE':
        user = request.user
        try:
            DeliveryAddress.address_list.filter(user=user, pk=da_id).delete()
            return Response({'message': 'Delivery address deleted'}, status=status.HTTP_200_OK)
        except DeliveryAddress.DoesNotExist:
            return Response({'message': 'Recipe not found'}, status=status.HTTP_200_OK)
        # end try-except
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def check_session(request):
    '''
    Backend endpoint to test validity of JWT
    '''
    return Response(status=status.HTTP_200_OK)
# end def
