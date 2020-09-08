from django.db import models
from django.utils import timezone

import uuid


class Recipe(models.Model):
    recipe_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    recipe_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    fulfillment_date = models.DateField()
    estimated_price_start = models.DecimalField(decimal_places=2, max_digits=6)
    estimated_price_end = models.DecimalField(decimal_places=2, max_digits=6)
    final_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)

    # recipe owner, set null when user is deleted
    owner = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)

    # temp model for vendor, set null when vendor is deleted
    vendor = models.ForeignKey('users.Vendor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.recipe_id}: {self.recipe_name} created on {self.date_created}'
    # end def

# end class


class Ingredient(models.Model):
    ing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    foreign_id = models.CharField(max_length=50, editable=False)  # foreign key id on ingredient in vendor database
    ing_name = models.CharField(max_length=200)
    image_url = models.URLField(max_length=300)
    category = models.CharField(max_length=100)
    metadata = models.JSONField()  # stores metadata json from NTUC

    # recipe ref
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ing_name} from {self.category} created in {self.date_created}'
    # end def

# end class
