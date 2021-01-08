from django.contrib import admin
from .models import(CoreLevelPlans, CoreBrand, Ewallet, UnilevelNetwork,
                    Rewards, PayoutReport, DepositReport, AffilatePlans, TestNetwork)
from accounts.models import Rank


class LvlAdmin(admin.ModelAdmin):
    list_display = ('marketing_plan', 'affilate', 'user',)


class LayerAdmin(admin.ModelAdmin):
    list_display = ('marketing_plan', 'affilate', 'user', 'parent')
    pass

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
