from django.contrib import admin
from .models import(CoreLevelPlans, CoreBrand, Ewallet, UnilevelNetwork, UserMessages, Marketingwallet,
                    Rewards, PayoutReport, DepositReport, AffilatePlans, TestNetwork, CoreDocs, CoreMarketingSetting,
                    CoreTestMpttNode, CoreMlmOrders, CoreVendorMlmOrders, BillingInfo, CoreVendorTestMpttNode, RewardsReport)
from accounts.models import Rank


class CoreMarketingSettingAdmin(admin.ModelAdmin):
    list_display = ('final', 'pv_rate_etb',)


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
                    'order_status', 'payment_type', 'reference_no', 'paid_already',)


class CoreMlmOrdersAdmin(admin.ModelAdmin):
    list_display = ('ordered_by', 'product',
                    'order_status', 'payment_type', 'reference_no', 'paid_already','timestamp',)
    list_editable = ('order_status', )
    search_fields =['ordered_by__username',]
    # list_editable = ('affilate',)


class MarketingWalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_id', 'user', 'amount', 'pv_count', )
    list_editable = ('amount', 'pv_count',)


class AffilatePlansAdmin(admin.ModelAdmin):
    list_display = ('plan_id', 'affilate', 'plan_type', 'core_plan', 'vendor_plan', 'total_earned',
                    'total_downline', 'total_direct_referrals', 'total_earned_pv', 'timestamp',)
    search_fields = ['affilate__user__username', ]


class RewardsReportAdmin(admin.ModelAdmin):
    list_display = ('reward', 'affilate', 'timestamp',)


admin.site.register(CoreLevelPlans)
admin.site.register(CoreBrand)
admin.site.register(Ewallet)
admin.site.register(Marketingwallet, MarketingWalletAdmin)
admin.site.register(UnilevelNetwork, LvlAdmin)
admin.site.register(Rank)
admin.site.register(Rewards)
admin.site.register(PayoutReport)
admin.site.register(DepositReport)
admin.site.register(AffilatePlans, AffilatePlansAdmin)
admin.site.register(TestNetwork,  LayerAdmin)
admin.site.register(UserMessages, UserMessagesAdmin)
admin.site.register(CoreDocs)
admin.site.register(CoreTestMpttNode, CoreTestMpttNodeAdmin)
admin.site.register(CoreVendorMlmOrders, CoreVendorMlmOrdersAdmin)
admin.site.register(CoreMlmOrders, CoreMlmOrdersAdmin)
admin.site.register(BillingInfo)
admin.site.register(RewardsReport, RewardsReportAdmin)
admin.site.register(CoreVendorTestMpttNode, CoreVendorTestMpttNodeAdmin)
admin.site.register(CoreMarketingSetting, CoreMarketingSettingAdmin)
