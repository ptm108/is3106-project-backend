from django.db import transaction
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Groupbuy
from .serializers import GroupbuySerializer


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
    Supports filter, orderby and pagination (pagesize, page)
    """

    if request.method == 'GET':
        groupbuys = Groupbuy.groupbuys.all()

        # get all params from request, None otherwise
        after_date = request.query_params.get('afterdate', None)
        before_date = request.query_params.get('beforedate', None)
        order_by = request.query_params.get('orderby', None)

        # get pagination params from request, default is (10, 1)
        page_size = request.query_params.get('pagesize', 10)
        page = request.query_params.get('page', 1)


        serializer = GroupbuySerializer(groupbuys, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if 

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def
