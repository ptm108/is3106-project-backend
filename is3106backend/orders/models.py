from django.db import models
import uuid

class GroupBuy(models.Model):
    gb_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    current_order_quantity = models.PositiveIntegerField(default=0)
    minimum_order_quantity = models.PositiveIntegerField(blank=True)
    approval_status = models.BooleanField(default=False)
    order_by = models.DateTimeField()

    # Recipe ref
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.SET_NULL, null=True)

    # Enum for group-buy status
    GROUPBUY_STATE_CHOICES = [
        ('GROUPBUY_IN_PROGRESS', 'GROUPBUY_IN_PROGRESS'),
        ('GROUPBUY_EXPIRED', 'GROUPBUY_EXPIRED'),
        ('DELIVERY_IN_PROGRESS', 'DELIVERY_IN_PROGRESS'),
        ('DELIVERED', 'DELIVERED')
    ]
    status = models.CharField(
        max_length=20,
        choices=GROUPBUY_STATE_CHOICES,
        default='PENDING_APPROVAL'
    )

# end class
