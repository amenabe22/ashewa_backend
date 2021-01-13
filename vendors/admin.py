from django.contrib import admin
from .models import Vendor, VendorLevelPlans, Order, Cart


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product','order_status', 'timestamp',)
    list_editable = ('order_status',)


admin.site.register(Vendor)
admin.site.register(VendorLevelPlans)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Cart)
