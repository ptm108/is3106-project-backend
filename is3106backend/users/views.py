from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import logging

# getting instance of logger
logger = logging.getLogger(__name__)

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request.user)
        content = {'message': 'Hello, World!'}
        return Response(content)
