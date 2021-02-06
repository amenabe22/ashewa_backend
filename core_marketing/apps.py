from django.apps import AppConfig


class CoreMarketingConfig(AppConfig):
    name = 'core_marketing'

    def ready(self):
        import core_marketing.signals
