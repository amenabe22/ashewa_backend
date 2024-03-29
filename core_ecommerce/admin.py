from django.contrib import admin
from .models import (ParentCategory, Category, SubCategory,
                     Products, ProductImage, LandingCarousel, PaymentType)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'selling_price','vendor', 'product_parent_category','stock_amount',)

admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Products, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(LandingCarousel)
admin.site.register(PaymentType)