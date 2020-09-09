from django.contrib import admin
from .models import Groupbuy, Order


class GroupbuyAdmin(admin.ModelAdmin):
    list_display = ('gb_id', 'recipe', 'current_order_quantity', 'minimum_order_quantity', 'order_by', 'approval_status')
# end class

class OrderAdmin(admin.ModelAdmin):
    list_display = ('o_id', 'order_quantity', 'buyer', 'delivery_address', 'order_date', 'groupbuy')
# end class

admin.site.register(Groupbuy, GroupbuyAdmin)
admin.site.register(Order, OrderAdmin)
