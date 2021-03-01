from .models import CoreMarketingSetting


def get_pv_rate():
    pv_etb_rate = 3
    marketing_setting = CoreMarketingSetting.objects.filter(
        final=True)

    if marketing_setting.exists():
        pv_etb_rate = marketing_setting[0].pv_rate_etb
    return pv_etb_rate
