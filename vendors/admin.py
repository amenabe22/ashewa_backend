from django.contrib import admin
from .models import Vendor, VendorLevelPlans, Order, Cart,VenodrGallery


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id','order_status', 'timestamp',)
    list_editable = ('order_status',)


admin.site.register(Vendor)
admin.site.register(VendorLevelPlans)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Cart)
admin.site.register(VenodrGallery)
