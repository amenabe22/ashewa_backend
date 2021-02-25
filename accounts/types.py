import graphene
from graphene_django import DjangoObjectType
from .models import CustomUser, Admin, Affilate, UserProfile
from vendors.models import Vendor
from django.core.cache import cache
from uuid import uuid4


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
        # init caching
        # setup request specific cache key 
        cache_key = str(info.context.user.user_id)
        # parse cache 
        stats = cache.get(cache_key)
        # pull data from cache if it's available 
        if stats is not None:
            return stats
        stats = [
            {'stat': is_vendor, 'ptype': 'vendor'},
            {'stat': is_admin, 'ptype': 'admin'},
            {'stat': is_affilate, 'ptype': 'affilate'}]
        # store in cache if not available 
        cache.set(cache_key, stats, 30)

        return stats


class AffilateType(DjangoObjectType):
    class Meta:
        model = Affilate


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class DescUsersType(graphene.ObjectType):
    user = graphene.Field(CoreUsersType)
    profile = graphene.Field(UserProfileType)

    @graphene.resolve_only_args
    def resolve_user(self):
        return self.user

    @graphene.resolve_only_args
    def resolve_profile(self):
        return self.profile
