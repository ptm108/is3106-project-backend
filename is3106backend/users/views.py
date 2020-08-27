from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import CustomUserSerializer

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    #end def
#end class


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Marks user as deleted when called
    """
    
    if request.method == 'POST':
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
        #end try-except
    #end if

#end def
