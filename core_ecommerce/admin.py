from django.contrib import admin
from .models import (ParentCategory, Category, SubCategory,
                     Products, ProductImage, LandingCarousel)

admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Products)
admin.site.register(ProductImage)
admin.site.register(LandingCarousel)