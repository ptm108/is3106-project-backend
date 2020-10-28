from django.db import models
from django.utils import timezone

import uuid

def recipe_directory_path(instance, filename):
    return 'recipe_{0}/{1}'.format(instance.recipe_id, filename)
# end def

class Recipe(models.Model):
    recipe_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    recipe_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    estimated_price_start = models.DecimalField(decimal_places=2, max_digits=6)
    estimated_price_end = models.DecimalField(decimal_places=2, max_digits=6)
    deleted = models.BooleanField(default=False)

    # recipe display photo
    display_photo = models.ImageField(upload_to=recipe_directory_path, max_length=100, blank=True, null=True, default='')

    # recipe owner, set null when user is deleted
    owner = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)

    # recipe model manager
    recipe_book = models.Manager()

    def __str__(self):
        return f'{self.recipe_name}; {self.date_created.date()}'
    # end def

# end class


class Ingredient(models.Model):
    ing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    foreign_id = models.CharField(max_length=50, editable=False)  # foreign key id on ingredient in vendor database
    ing_name = models.CharField(max_length=200)
    image_url = models.URLField(max_length=300)
    category = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100, default="")
    selling_price = models.DecimalField(decimal_places=2, max_digits=6)
    estimated_price = models.DecimalField(decimal_places=2, max_digits=6)
    metadata = models.JSONField()  # stores metadata json from vendor

    # recipe ref
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ingredients')

    ingredient_list = models.Manager()

    def __str__(self):
        return f'{self.ing_name} ({self.category}) created in {self.date_created}'
    # end def

# end class
