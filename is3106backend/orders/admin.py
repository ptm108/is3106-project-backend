from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('o_id', 'order_quantity', 'buyer', 'delivery_address', 'order_date', 'groupbuy')
# end class

admin.site.register(Order, OrderAdmin)
