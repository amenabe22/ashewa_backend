from django.contrib import admin
from .models import(CoreLevelPlans, CoreBrand, Ewallet, UnilevelNetwork, UserMessages, Marketingwallet,
                    Rewards, PayoutReport, DepositReport, AffilatePlans, TestNetwork, CoreDocs,
                    CoreTestMpttNode, CoreMlmOrders, CoreVendorMlmOrders, BillingInfo, CoreVendorTestMpttNode)
from accounts.models import Rank


class LvlAdmin(admin.ModelAdmin):
    list_display = ('marketing_plan', 'affilate', 'user',)


class LayerAdmin(admin.ModelAdmin):
    list_display = ('marketing_plan', 'affilate',
                    'user', 'parent', 'layer_id',)


class CoreTestMpttNodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'marketing_plan', 'level', 'parent', )


class CoreVendorTestMpttNodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'marketing_plan', 'level', 'parent', )


class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message',)


class CoreVendorMlmOrdersAdmin(admin.ModelAdmin):
    list_display = ('ordered_by', 'product',
                    'order_status', 'paid_already',)


class CoreMlmOrdersAdmin(admin.ModelAdmin):
    list_display = ('ordered_by', 'product',
                    'order_status', 'paid_already',)
    list_editable = ('order_status', )
    # list_editable = ('affilate',)
admin.site.register(CoreLevelPlans)
admin.site.register(CoreBrand)
admin.site.register(Ewallet)
admin.site.register(Marketingwallet
                    )
admin.site.register(UnilevelNetwork, LvlAdmin)
admin.site.register(Rank)
admin.site.register(Rewards)
admin.site.register(PayoutReport)
admin.site.register(DepositReport)
admin.site.register(AffilatePlans)
admin.site.register(TestNetwork,  LayerAdmin)
admin.site.register(UserMessages, UserMessagesAdmin)
admin.site.register(CoreDocs)
admin.site.register(CoreTestMpttNode, CoreTestMpttNodeAdmin)
admin.site.register(CoreVendorMlmOrders, CoreVendorMlmOrdersAdmin)
admin.site.register(CoreMlmOrders, CoreMlmOrdersAdmin)
admin.site.register(BillingInfo)
admin.site.register(CoreVendorTestMpttNode, CoreVendorTestMpttNodeAdmin)
