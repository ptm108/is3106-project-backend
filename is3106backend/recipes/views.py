from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import json

from .models import Recipe, Ingredient
# from .serializers import CustomUserSerializer


class DefaultView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Recipes Base URL'}
        return Response(content)
    # end def
# end class


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_recipe(request):
    """
    Creates a new recipe and required ingredients
    """

    if request.method == 'POST':
        user = request.user
        data = request.data
        res = {}

        # start atomic transaction to create recipe and required ingredients
        with transaction.atomic():
            print(data['fulfillment_date'])
            recipe = Recipe(
                recipe_name=data['recipe_name'],
                fulfillment_date=data['fulfillment_date'],
                estimated_price_start=data['estimated_price_start'],
                estimated_price_end=data['estimated_price_end'],
                owner=user
            )
            recipe.save()

            for ing in data['ingredients']:
                ingredient = Ingredient(
                    foreign_id=ing['foreign_id'],
                    ing_name=ing['ing_name'],
                    image_url=ing['image_url'],
                    category=ing['category'],
                    metadata=json.dumps(ing['metadata']),
                    recipe=recipe
                )
                ingredient.save()
            # end for

        # end with
        return Response({'message': 'Recipe created'}, status=status.HTTP_200_OK)
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)

# end def
