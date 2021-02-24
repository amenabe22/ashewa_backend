import graphene
from .types import CoreUsersType, UserProfileType
from .models import CustomUser, Affilate, UserProfile
from graphene_file_upload.scalars import Upload
from core_marketing.models import Marketingwallet, Ewallet
from django_graphene_permissions.permissions import permissions_checker, IsAuthenticated


class NewUserMutation(graphene.Mutation):
    payload = graphene.Field(CoreUsersType)

    class Arguments:
        # either of these
        full_name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, full_name, email, password):
        if(CustomUser.objects.filter(email=email).exists()):
            raise Exception("email is duplicate")
        if(CustomUser.objects.filter(username=email).exists()):
            raise Exception("username is duplicate")
        user = CustomUser.objects.create(
            username=email, email=email,
            full_name=full_name
        )
        user.set_password(password)
        user.save()
        Marketingwallet.objects.create(
            user=user
        )
        Ewallet.objects.create(user=user)
        Affilate.objects.create(user=user)
        return NewUserMutation(payload=user)


class EditProfile(graphene.Mutation):
    payload = graphene.Field(CoreUsersType)

    class Arguments:
        full_name = graphene.String()
        email = graphene.String()
        username = graphene.String()
        phone = graphene.String()

    def mutate(self, info, username,  full_name, email, phone):
        user = CustomUser.objects.filter(user_id=info.context.user.user_id)
        # user.set_password(password=password)
        if not user.exists():
            raise Exception("user not found")
        user.update(username=username, phone=phone,
                    full_name=full_name, email=email)
        return EditProfile(payload=user[0])


class ChangePasswordMutation(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        password = graphene.String()

    def mutate(self, info, password):
        user = CustomUser.objects.get(user_id=info.context.user.user_id)
        user.set_password(password)
        user.save()

        return ChangePasswordMutation(payload=True)


class UpdateProfilePic(graphene.Mutation):
    payload = graphene.Field(UserProfileType)

    class Arguments:
        pic = Upload()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, pic, upload):
        profile = UserProfile.objects.filter(user=info.context.user)
        if not profile.exists():
            prof = UserProfile.objects.create(user=info.context.user)
        else:
            prof = profile[0]
        prof.profile_pic = pic
        prof.save()
        return UpdateProfilePic(payload=prof)
