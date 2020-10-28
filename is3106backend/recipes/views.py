from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone

from datetime import datetime, timedelta
import json
from pytz import utc

from .models import Recipe, Ingredient
from orders.models import Groupbuy
from .serializers import RecipeSerializer, IngredientSerializer


class DefaultView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Recipes Base URL'}
        return Response(content)
    # end def
# end class


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
@parser_classes((MultiPartParser, FormParser,))
def protected_recipe_view(request):
    '''
    Retrieves all recipes created by user making request
    '''
    if request.method == 'GET':
        user = request.user
        try:
            recipes = Recipe.recipe_book.filter(owner=user)
            
            search = request.GET.get('search')
            
            if search is not None:
                recipes = recipes.filter(recipe_name__icontains=search).order_by('-date_created')
            
            paginator = Paginator(recipes, 10)
            
            page_number = request.GET.get('page')
            
            page_obj = paginator.get_page(page_number)

            serializer = RecipeSerializer(page_obj, many=True, context={"request": request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response({'message': 'No recipes found'}, status=status.HTTP_200_OK)
        # end try-except
    # end if


    """
    Creates a new recipe and required ingredients
    """
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.data['data'])

        # date validation
        f_date = utc.localize(datetime.strptime(data['fulfillment_date'], '%Y-%m-%d'))

        if timezone.now() > f_date:
            return Response({'message': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)
        # end if

        # start atomic transaction to create recipe and required ingredients
        with transaction.atomic():
            # create recipe
            recipe = Recipe(
                recipe_name=data['recipe_name'],
                estimated_price_start=data['estimated_price_start'],
                estimated_price_end=data['estimated_price_end'],
                owner=user
            )

            if 'display_photo' in request.data:
                recipe.display_photo = request.data['display_photo']
            # end if

            recipe.save()

            # create necessary ingredients
            for ing in data['ingredients']:
                ingredient = Ingredient(
                    foreign_id=ing['foreign_id'],
                    ing_name=ing['ing_name'],
                    image_url=ing['image_url'],
                    category=ing['category'],
                    quantity=ing['quantity'],
                    selling_price=ing['selling_price'],
                    estimated_price=ing['estimated_price'],
                    metadata=json.dumps(ing['metadata']),
                    recipe=recipe
                )
                ingredient.save()
            # end for

            # create groupbuy associated to this recipe
            groupbuy = Groupbuy(
                fulfillment_date=f_date,
                order_by=f_date-timedelta(days=2),  # max order-by date is 2 days before fulfillment date
                recipe=recipe
            )
            groupbuy.save()
        # end with

        return Response({
            'message': 'Recipe created',
            "recipe_id": recipe.recipe_id,
            "gb_id": groupbuy.gb_id
        }, status=status.HTTP_200_OK)
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_recipe(request, pk):
    '''
    Marks a recipe as deleted
    HOWEVER, if group buy has been approved, it will still proceed accordingly
    '''
    if request.method == 'DELETE':
        user = request.user
        try:
            Recipe.recipe_book.filter(owner=user, pk=pk).update(deleted=True)
            return Response({'message': 'Recipe deleted'}, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response({'message': 'Recipe not found'}, status=status.HTTP_200_OK)
        # end try-except
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def undelete_recipe(request, pk):
    '''
    EXPERIMENTAL METHOD
    Undeletes a recipe
    No effect on group buys
    '''
    if request.method == 'POST':
        user = request.user
        try:
            Recipe.recipe_book.filter(owner=user, pk=pk).update(deleted=False)
            return Response({'message': 'Recipe undeleted'}, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response({'message': 'Recipe not found'}, status=status.HTTP_200_OK)
        # end try-except
    # end if

    return Response({'message': 'Request Declined'}, status=status.HTTP_400_BAD_REQUEST)
# end def