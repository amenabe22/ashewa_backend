import graphene
from graphene_django import DjangoObjectType
from .models import(ProductImage, Products, ParentCategory,
                    Category, SubCategory, LandingCarousel, ParentCategory)

from vendors.types import OrdersType
from core_marketing.types import CoreMlmOrderType


class LandingCarsType(DjangoObjectType):
    class Meta:
        model = LandingCarousel


class ParentCategoryType(DjangoObjectType):
    class Meta:
        model = ParentCategory


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage


class ProductsType(DjangoObjectType):
    product_images = graphene.List(ProductImageType)

    @graphene.resolve_only_args
    def resolve_product_images(self):
        return self.product_images.all()

    class Meta:
        model = Products


class SubCatsType(DjangoObjectType):
    class Meta:
        model = SubCategory


class ProductsPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(ProductsType)
    total = graphene.Int()


class LandingCatBlockType(graphene.ObjectType):
    pcat = graphene.Field(ParentCategoryType)
    catProds = graphene.List(ProductsType)


class UsrOrderType(graphene.ObjectType):
    core_ord = graphene.List(CoreMlmOrderType)
    ords = graphene.List(OrdersType)
