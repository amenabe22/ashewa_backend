import graphene
from .types import CoreUsersType
from .models import CustomUser, Affilate
from core_marketing.models import Marketingwallet, Ewallet


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
