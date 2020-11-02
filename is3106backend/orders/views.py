from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def protected_order_view(request):
    '''
    Gets all orders created by user
    '''
    if request.method == 'GET':
        user = request.user

        try:
            orders = Order.orders.filter(buyer=user)

            serializer = OrderSerializer(orders, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    return Response({'message': 'Unsupported'}, status=status.HTTP_400_BAD_REQUEST)
# end def
