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

    # # Enum for group-buy status
    # GROUPBUY_STATE_CHOICES = [
    #     ('GROUPBUY_IN_PROGRESS', 'GROUPBUY_IN_PROGRESS'),
    #     ('GROUPBUY_EXPIRED', 'GROUPBUY_EXPIRED'),
    #     ('DELIVERY_IN_PROGRESS', 'DELIVERY_IN_PROGRESS'),
    #     ('DELIVERED', 'DELIVERED')
    # ]
    # status = models.CharField(
    #     max_length=20,
    #     choices=GROUPBUY_STATE_CHOICES,
    #     default='PENDING_APPROVAL'
    # )

    # method to get groupbuy status
    def get_status(self):
        if timezone.now() > recipe.fulfillment_date:
            return "GROUPBUY_EXPIRED" if not self.approval_status else "DELIVERED"
        # end if

        if not self.approval_status:
            return "PENDING_APPROVAL"
        # end if

        if timezone.now() < self.order_by:
            return "GROUPBUY_IN_PROGRESS"
        # end if 

        return "DELIVERY_IN_PROGRESS"
    # end def

    def __str__(self):
        return f'Groupbuy ID: {self.gb_id}'
    # end def
# end class
