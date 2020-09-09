from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
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
    Supports search (name), filtering (approved, upcoming), 
    and pagination (pagesize, page)
    """

    if request.method == 'GET':
        groupbuys = Groupbuy.groupbuys.all()

        # extract params
        try:
            # get all params from request, None otherwise
            approved = int(request.query_params.get('approved', 0)) # 1 => approved, -1 => unapproved
            upcoming = int(request.query_params.get('upcoming', 1)) # 1 => true

            # get pagination params from request, default is (10, 1)
            page_size = int(request.query_params.get('pagesize', 10))

            # get search value from params
            search = request.query_params.get('search', None)

        except ValueError:
            return Response({'message': 'Check your params'}, status=status.HTTP_400_BAD_REQUEST) 
        #end try-except

        if approved > 0: groupbuys = groupbuys.filter(approval_status=True)
        if approved < 0: groupbuys = groupbuys.filter(approval_status=False)
        if search is not None: groupbuys = groupbuys.filter(recipe__recipe_name__icontains=search)

        # paginator configs
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        result_page = paginator.paginate_queryset(groupbuys, request)

        serializer = GroupbuySerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    # end if 

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def
