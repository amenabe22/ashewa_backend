from django.contrib import admin
from .models import Vendor, VendorLevelPlans, Order, Cart, VenodrGallery, VendorData, Social, VendorCeoImgs, Promotions


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_status', 'timestamp', 'product','ordered_by',
                    'reference_no', 'payment_type',)
    list_editable = ('order_status',)


admin.site.register(Vendor)
admin.site.register(VendorLevelPlans)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Cart)
admin.site.register(VenodrGallery)
admin.site.register(VendorData)
admin.site.register(Social)
admin.site.register(VendorCeoImgs)
admin.site.register(Promotions)
