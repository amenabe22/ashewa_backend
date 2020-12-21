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


class VendorValueTypes(graphene.ObjectType):
    val = graphene.List(VendorPlanType)
    taken = graphene.Boolean()


class VendorPlanPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(VendorValueTypes)
    total = graphene.Int()
