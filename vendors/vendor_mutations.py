import graphene
from graphene_file_upload.scalars import Upload
from vendors.models import Vendor, VendorLevelPlans
from .models import VendorLevelPlans, Vendor, Order, Cart, VenodrGallery
from django_graphene_permissions import permissions_checker
from ashewa_final.core_perimssions import VendorsPermission, AdminPermission
from django_graphene_permissions.permissions import IsAuthenticated
from core_ecommerce.models import Products


class PopCart(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        cart = graphene.String()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, cart):
        usrCart = Cart.objects.filter(
            cart_core_id=cart, user=info.context.user)
        if usrCart.exists():
            usrCart.delete()
        else:
            raise Exception("invalid cart")

        return PopCart(payload=True)


class LoadCart(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        product = graphene.String()
        quan = graphene.Int()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, product, quan):
        try:
            prd = Products.objects.get(product_id=product)
            Cart.objects.create(user=info.context.user,
                                product=prd, quantity=quan)
        except Exception as e:
            raise Exception(e)

        return LoadCart(payload=True)


class CreateOrder(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        product = graphene.String()

    @permissions_checker([VendorsPermission, IsAuthenticated])
    def mutate(self, info, product):
        # create the order here
        try:
            prd = Products.objects.get(product_id=product)
            Order.objects.create(
                product=prd, ordered_by=info.context.user,
                ordered_from=prd.vendor
            )
        except Exception as e:
            raise Exception(str(e))

        return CreateOrder(payload=True)


class UpdateStoreCover(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        pic = Upload()

    @permissions_checker([VendorsPermission])
    def mutate(self, info, pic):
        try:
            vend = Vendor.objects.get(
                user=info.context.user
            )
            vend.store_cover = pic
            vend.save()
        except Exception as e:
            raise Exception(str(e))

        return UpdateStoreCover(payload=True)


class CreateVendorPlans(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        plan_name = graphene.String()
        plan_description = graphene.String()
        purchase_bonus = graphene.String()
        level1_percentage = graphene.String()
        level2_percentage = graphene.String()
        level3_percentage = graphene.String()
        level4_percentage = graphene.String()
        level5_percentage = graphene.String()
        level6_percentage = graphene.String()
        level7_percentage = graphene.String()
        level8_percentage = graphene.String()
        level9_percentage = graphene.String()
        level10_percentage = graphene.String()
        level11_percentage = graphene.String()
        level12_percentage = graphene.String()
        level13_percentage = graphene.String()
        level14_percentage = graphene.String()
        level15_percentage = graphene.String()

    @permissions_checker([VendorsPermission])
    def mutate(self, plan_name, plan_description, purchase_bonus, level1_percentage, level2_percentage, level3_percentage,
               level4_percentage, level5_percentage,
               level6_percentage, level7_percentage, level8_percentage, level9_percentage,
               level10_percentage, level11_percentage,
               level12_percentage, level13_percentage, level14_percentage, level15_percentage):
        pass
        return CreateVendorPlans(payload=True)

# class CreateVenodrGallery(graphene.Mutation):
#     payload = graphene.Boolean()

#     class Arguments:
#         image = Upload()
#         img_desc = graphene.String()

#         @permissions_checker([VendorsPermission])
#         def mutate(self, info, image, img_desc):
#             vendG = VenodrGallery.objects.all()
#             vendG.image = image
#             img_desc = img_desc
