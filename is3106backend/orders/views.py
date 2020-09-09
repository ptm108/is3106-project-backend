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
    """

    if request.method == 'GET':
        groupbuys = Groupbuy.groupbuys.all()
        serializer = GroupbuySerializer(groupbuys, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    # end if 

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def