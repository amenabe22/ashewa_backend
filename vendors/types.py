import graphene
from graphene_django import DjangoObjectType
from .models import Vendor, VendorLevelPlans, Cart, Order, VenodrGallery

class VenodrGalleryType(DjangoObjectType):
    class Meta:
        model = VenodrGallery
        fields = '__all__'

class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        fields = '__all__'


class VendorPlanType(DjangoObjectType):
    class Meta:
        model = VendorLevelPlans
        fields = '__all__'

class VendorOverviewDataType(graphene.ObjectType):
    val = graphene.String()
    label = graphene.String()

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


class OrdersType(DjangoObjectType):
    class Meta:
        model = Order


class CartsType(DjangoObjectType):
    class Meta:
        model = Cart


class CartPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(CartsType)
    total = graphene.Int()


class OrdersPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(OrdersType)
    total = graphene.Int()


