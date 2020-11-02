from django.db import models
from django.utils import timezone
import uuid


class Order(models.Model):
    o_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    order_date = models.DateTimeField(default=timezone.now, editable=False)
    order_quantity = models.PositiveSmallIntegerField()
    order_price = models.DecimalField(decimal_places=2, max_digits=6)
    contact_number = models.CharField(max_length=15, null=True)

    # user who placed order, deleted when user is deleted
    buyer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True)

    # delivery address of buyer, set null when delivery address is deleted
    delivery_address = models.ForeignKey('users.DeliveryAddress', on_delete=models.SET_NULL, null=True)

    # group buy ref, set null when group buy is deleted
    groupbuy = models.ForeignKey('groupbuys.Groupbuy', on_delete=models.SET_NULL, null=True)

    orders = models.Manager()

    def __str__(self):
        return f'Order ID: {self.o_id}'
    # end def
# end class
