from django.contrib import admin
from .models import Groupbuy


class GroupbuyAdmin(admin.ModelAdmin):
    list_display = ('gb_id', 'recipe', 'current_order_quantity', 'minimum_order_quantity', 'order_by', 'approval_status')
# end class

admin.site.register(Groupbuy, GroupbuyAdmin)
