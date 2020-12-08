# your_app/signals.py
from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from .models import CustomUser

post_save.connect(post_save_subscription, sender=CustomUser, dispatch_uid="accounts_post_save")
post_delete.connect(post_delete_subscription, sender=CustomUser, dispatch_uid="accounts_post_delete")
