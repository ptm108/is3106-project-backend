from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Groupbuy, Order
from .serializers import GroupbuySerializer
from users.models import DeliveryAddress

from datetime import datetime
from pytz import utc


class DefaultView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Orders Base URL'}
        return Response(content)
    # end def
# end class


@api_view(['GET'])
@permission_classes((AllowAny,))
def all_groupbuys(request):
    """
    Retrieves all groupbuys
    Supports search (name), filtering (approved, upcoming), 
    and pagination (pagesize, page)
    """

    if request.method == 'GET':
        groupbuys = Groupbuy.groupbuys.all()

        # extract params
        try:
            # get all params from request, None otherwise
            approved = int(request.query_params.get('approved', 0))  # 1 => approved, -1 => unapproved
            upcoming = int(request.query_params.get('upcoming', 1))  # 1 => true

            # get pagination params from request, default is (10, 1)
            page_size = int(request.query_params.get('pagesize', 10))

            # get search value from params
            search = request.query_params.get('search', None)

        except ValueError:
            return Response({'message': 'Check your params'}, status=status.HTTP_400_BAD_REQUEST)
        # end try-except

        if approved > 0:
            groupbuys = groupbuys.filter(approval_status=True)
        if approved < 0:
            groupbuys = groupbuys.filter(approval_status=False)
        if search is not None:
            groupbuys = groupbuys.filter(recipe__recipe_name__icontains=search)

        # paginator configs
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        result_page = paginator.paginate_queryset(groupbuys, request)

        serializer = GroupbuySerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def approve_groupbuy(request, pk):
    """
    Toggles groupbuy's approval status
    Only accessible by vendors
    """

    if request.method == 'PATCH':
        try:
            groupbuy = Groupbuy.groupbuys.get(pk=pk)
            groupbuy.approval_status = not groupbuy.approval_status
            groupbuy.save()
            return Response({
                'gb_id': groupbuy.gb_id,
                'approval_status': groupbuy.approval_status
            }, status=status.HTTP_200_OK)
        except Groupbuy.DoesNotExist:
            return Response({'message': 'Groupbuy not found'}, status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    return Response({'message': 'Unsupported'}, status=status.HTTP_400_BAD_REQUEST)
# end def


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def update_groupbuy(request, pk):
    """
    Updates groupbuy minimum order quantity, order by date, final price
    Only accessible by vendors
    """

    data = request.data

    if request.method == 'PATCH':
        try:
            moq, order_by, final_price = int(data['minimum_order_quantity']), datetime.strptime(data['order_by'], '%Y-%m-%d'), float(data['final_price'])
        except ValueError:
            return Response({'message': 'Check your data'}, status=status.HTTP_400_BAD_REQUEST)
        # end try-except

        try:
            Groupbuy.groupbuys.filter(pk=pk).update(minimum_order_quantity=moq, order_by=order_by, final_price=final_price)
            groupbuy = Groupbuy.groupbuys.get(pk=pk)
            
            serializer = GroupbuySerializer(groupbuy)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Groupbuy.DoesNotExist:
            return Response({'message': 'Groupbuy not found'}, status=status.HTTP_400_BAD_REQUEST)
        # end try-except
    # end if

    return Response({'message': 'Unsupported'}, status=status.HTTP_400_BAD_REQUEST)
# end def


@api_view(['POST', 'PATCH'])
@permission_classes((IsAuthenticated,))
def create_order(request):
    """
    Creates a new order
    """

    user = request.user
    data = request.data

    if request.method == 'POST':
        try:
            delivery_address = DeliveryAddress.address_list.get(pk=data['add_id'])
            groupbuy = Groupbuy.groupbuys.get(pk=data['gb_id'])
        except ObjectDoesNotExist:
            return Response({'message': 'Check your Groupbuy and Address ids'}, status=status.HTTP_400_BAD_REQUEST)
        # end try-except

        # check if groupbuy status
        if groupbuy.get_status() != "GROUPBUY_IN_PROGRESS":
            return Response({'message': 'Groupbuy is not available'}, status=status.HTTP_400_BAD_REQUEST)
        # end if

        # start atomic transaction to create order
        with transaction.atomic():
            new_order = Order(
                order_quantity=int(data['order_quantity']),
                order_price=groupbuy.final_price * float(data['order_quantity']),
                delivery_address=delivery_address,
                buyer=user,
                groupbuy=groupbuy
            )
            new_order.save()

            groupbuy.current_order_quantity = groupbuy.current_order_quantity + int(data['order_quantity'])
            groupbuy.save()

            return Response({
                'message': 'Order created',
                'o_id': new_order.o_id
            }, status=status.HTTP_200_OK)
        # end with
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def
