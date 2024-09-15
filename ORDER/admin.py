from django.contrib import admin
from .models import *
from django.utils.html import format_html

admin.site.register(Voucher)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'order_items_display')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]  


    def order_items_display(self, obj):
        items = obj.order_items.all()
        item_strs = [f"{item.shoe.name} (Size: {item.size.name}) " for item in items]
        return format_html("<br>".join(item_strs))

    order_items_display.short_description = 'Ordered Items'

admin.site.register(Order, OrderAdmin)
