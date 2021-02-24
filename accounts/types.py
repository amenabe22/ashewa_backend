import graphene
from graphene_django import DjangoObjectType
from .models import CustomUser, Admin, Affilate, UserProfile
from vendors.models import Vendor


class CoreUsersType(DjangoObjectType):
    class Meta:
        model = CustomUser


class PrivillageState(graphene.ObjectType):
    stat = graphene.Boolean()
    ptype = graphene.String()


class UsersDataType(DjangoObjectType):
    stats = graphene.List(PrivillageState)

    class Meta:
        model = CustomUser

    def resolve_stats(self, info):
        is_vendor = Vendor.objects.filter(user=info.context.user).exists()
        is_admin = Admin.objects.filter(user=info.context.user).exists()
        is_affilate = Affilate.objects.filter(user=info.context.user)
        return [
            {'stat': is_vendor, 'ptype': 'vendor'},
            {'stat': is_admin, 'ptype': 'admin'},
            {'stat': is_affilate, 'ptype': 'affilate'}]


class AffilateType(DjangoObjectType):
    class Meta:
        model = Affilate


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
