from vendors.models import Vendor
from accounts.models import Admin, Affilate
from django_graphene_permissions.permissions import BasePermission

class VendorsPermission(BasePermission):
    @staticmethod
    def has_permission(context):
        vendorStat = Vendor.objects.filter(user=context.user).exists()
        return vendorStat and context.user.is_authenticated

    @staticmethod
    def has_object_permission(context, obj):
        return True

class AdminPermission(BasePermission):
    @staticmethod
    def has_permission(context):
        adminStat = Admin.objects.filter(user=context.user).exists()
        return adminStat and context.user.is_authenticated 

    @staticmethod
    def has_object_permission(context, obj):
        return True

class AffilatePermission(BasePermission):
    @staticmethod
    def has_permission(context):
        adminStat = Affilate.objects.filter(user=context.user).exists()
        return adminStat and context.user.is_authenticated

    @staticmethod
    def has_object_permission(context, obj):
        return True
