from django.contrib import admin
from .models import(CoreLevelPlans, CoreBrand, Ewallet, UnilevelNetwork, UserMessages,
                    Rewards, PayoutReport, DepositReport, AffilatePlans, TestNetwork, CoreDocs)
from accounts.models import Rank


class LvlAdmin(admin.ModelAdmin):
    list_display = ('marketing_plan', 'affilate', 'user',)


class LayerAdmin(admin.ModelAdmin):
    list_display = ('marketing_plan', 'affilate',
                    'user', 'parent', 'layer_id',)


class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message',)
    # list_editable = ('affilate',)
admin.site.register(CoreLevelPlans)
admin.site.register(CoreBrand)
admin.site.register(Ewallet)
admin.site.register(UnilevelNetwork, LvlAdmin)
admin.site.register(Rank)
admin.site.register(Rewards)
admin.site.register(PayoutReport)
admin.site.register(DepositReport)
admin.site.register(AffilatePlans)
admin.site.register(TestNetwork,  LayerAdmin)
admin.site.register(UserMessages, UserMessagesAdmin)
admin.site.register(CoreDocs)
