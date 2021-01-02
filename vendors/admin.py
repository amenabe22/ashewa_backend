from django.contrib import admin
from .models import Vendor, VendorLevelPlans, Order, Cart

admin.site.register(Vendor)
admin.site.register(VendorLevelPlans)
admin.site.register(Order)
admin.site.register(Cart)
