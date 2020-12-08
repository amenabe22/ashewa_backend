from django.contrib import admin
from .models import(CoreLevelPlans, CoreBrand, Ewallet, UnilevelNetwork,
                    Rewards, PayoutReport, DepositReport)
from accounts.models import Rank


class LvlAdmin(admin.ModelAdmin):
    list_display = ('marketing_plan', 'affilate', 'user',)
    # list_editable = ('affilate',)
admin.site.register(CoreLevelPlans)
admin.site.register(CoreBrand)
admin.site.register(Ewallet)
admin.site.register(UnilevelNetwork, LvlAdmin)
admin.site.register(Rank)
admin.site.register(Rewards)
admin.site.register(PayoutReport)
admin.site.register(DepositReport)
