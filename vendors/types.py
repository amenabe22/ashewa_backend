import graphene
from .models import Vendor, VendorLevelPlans
from graphene_django import DjangoObjectType


class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        fields = '__all__'


class VendorPlanType(DjangoObjectType):
    class Meta:
        model = VendorLevelPlans
        fields = '__all__'
