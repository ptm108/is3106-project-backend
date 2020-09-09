from django.db import models
from django.utils import timezone

import uuid
from recipes.models import Recipe


class Groupbuy(models.Model):
    gb_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    current_order_quantity = models.PositiveIntegerField(default=0)
    minimum_order_quantity = models.PositiveIntegerField(blank=True, null=True)
    approval_status = models.BooleanField(default=False)
    order_by = models.DateTimeField()

    # Recipe ref
    recipe = models.OneToOneField(Recipe, on_delete=models.SET_NULL, null=True)

    groupbuys = models.Manager()

    # method to get groupbuy status
    def get_status(self):
        if timezone.now().date() > self.recipe.fulfillment_date: 
            return "GROUPBUY_EXPIRED" if not self.approval_status else "DELIVERED"
        # end if

        if not self.approval_status: return "PENDING_APPROVAL"
        if timezone.now() < self.order_by: return "GROUPBUY_IN_PROGRESS"

        return "DELIVERY_IN_PROGRESS"
    # end def

    def __str__(self):
        return f'Groupbuy ID: {self.gb_id}'
    # end def
# end class

class Order(models.Model):
    o_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    order_date = models.DateTimeField(default=timezone.now, editable=False)
    order_quantity = models.PositiveSmallIntegerField()
    delivery_address = models.CharField(max_length=200) # temp replacement
    order_price = models.DecimalField(decimal_places=2, max_digits=6)

    # user who placed order
    buyer = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Order ID: {self.o_id}'
    #end def
# end class
