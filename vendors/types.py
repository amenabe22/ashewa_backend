import graphene 
from .models import Vendor
from graphene_django import DjangoObjectType

class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        fields = '__all__'

