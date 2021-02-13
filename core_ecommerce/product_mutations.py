import graphene
from vendors.models import Vendor
from core_ecommerce.models import CoreBrand
from graphene_file_upload.scalars import Upload
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from ashewa_final.core_perimssions import AdminPermission, VendorsPermission
from .models import Products, ProductImage, ParentCategory, SubCategory, Category
from .types import ProductImageType, ProductsType, ParentCategoryType, CategoryType, SubCatsType


class EditProduct(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        product = graphene.String()
        product_name = graphene.String()
        product_desc = graphene.String()
        product_parent_category = graphene.String()
        product_category = graphene.String()
        product_sub_category = graphene.String()
        # product_brand = graphene.String()
        selling_price = graphene.Int()
        dealer_price = graphene.Int()
        business_value = graphene.Int()
        # discount = graphene.Int()
        stock_amount = graphene.Int()
        # tax = graphene.Int()
        images = Upload()

    @permissions_checker([VendorsPermission])
    def mutate(self, info, product_name, product_desc, product_parent_category, product_category,
               product_sub_category, selling_price, dealer_price, business_value, stock_amount, 
               images, product):
        vendor = Vendor.objects.get(user=info.context.user)
        prod = Products.objects.filter(product_id=product, vendor=vendor)
        if not prod.exists():
            raise Exception("product error")
        try:
            sc = SubCategory.objects.get(sub_cat_id=product_sub_category)
            cat = Category.objects.get(cat_id=product_category)
            parent = ParentCategory.objects.get(
                pcat_id=product_parent_category)
        except Exception as e:
            raise Exception(str(e))
        prod.update(vendor=vendor, product_name=product_name, product_desc=product_desc,
                    selling_price=selling_price, dealer_price=dealer_price,
                    business_value=business_value, discount=None,  # discount not set
                    stock_amount=stock_amount, product_parent_category=parent,
                    product_subcategory=sc, product_category=cat, tax=None,  # tax amount not set
                    )
        return EditProduct(payload=True)


class NewProductMutation(graphene.Mutation):
    payload = graphene.List(ProductsType)

    class Arguments:
        product_name = graphene.String()
        product_desc = graphene.String()
        product_parent_category = graphene.String()
        product_category = graphene.String()
        product_sub_category = graphene.String()
        # product_brand = graphene.String()
        selling_price = graphene.Int()
        dealer_price = graphene.Int()
        business_value = graphene.Int()
        # discount = graphene.Int()
        stock_amount = graphene.Int()
        # tax = graphene.Int()
        images = Upload()

    @permissions_checker([VendorsPermission])
    def mutate(self, info, product_name, product_desc, product_parent_category, product_category,
               product_sub_category, selling_price, dealer_price, business_value, stock_amount, images):
        try:
            sc = SubCategory.objects.get(sub_cat_id=product_sub_category)
            cat = Category.objects.get(cat_id=product_category)
            parent = ParentCategory.objects.get(
                pcat_id=product_parent_category)
        except Exception as e:
            raise Exception(str(e))
        # create product here
        prod = Products.objects.create(
            vendor=Vendor.objects.get(user=info.context.user),
            product_name=product_name, product_desc=product_desc,
            selling_price=selling_price, dealer_price=dealer_price,
            business_value=business_value, discount=None,  # discount not set
            stock_amount=stock_amount, product_parent_category=parent,
            product_subcategory=sc, product_category=cat, tax=None,  # tax amount not set
        )
        [prod.product_images.create(image=(x)) for x in images]
        return NewProductMutation(payload=Products.objects.filter(
            product_id=prod.product_id
        ))


class CreateParentCategory(graphene.Mutation):
    # payload = graphene.List(ParentCategoryType)
    status = graphene.String()

    class Arguments:
        pcat_name = graphene.String()
        brand = graphene.String()

    # only admins can do this
    @permissions_checker([AdminPermission])
    def mutate(self, info, pcat_name, brand):
        ParentCategory.objects.create(
            parent_cat_name=pcat_name, brand=CoreBrand.objects.get(
                brand_id=brand
            )
        )
        return CreateParentCategory(status="done")


class CreateCategory(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        cat_name = graphene.String()
        parent = graphene.String()

    # only admins can do this
    @permissions_checker([AdminPermission])
    def mutate(self, info, cat_name, parent):
        Category.objects.create(
            category_name=cat_name,
            parent_category=ParentCategory.objects.get(
                pcat_id=parent
            )
        )
        return CreateCategory(status="done")


class CreateSubCategory(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        scat_name = graphene.String()
        parent = graphene.String()

    # only admins can do this
    @permissions_checker([AdminPermission])
    def mutate(self, info, scat_name, parent):
        SubCategory.objects.create(
            sub_category_name=scat_name,
            category=Category.objects.get(
                cat_id=parent
            )
        )
        return CreateCategory(status="done")


class CreateBrand(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        brand_name = graphene.String()
        brand_desc = graphene.String()
        # brand_image = Upload()

    # only admins can do this
    @permissions_checker([AdminPermission])
    def mutate(self, info, brand_name, brand_description):
        CoreBrand.objects.create(
            brand_name=brand_name,
            brand_description=brand_description,
            # brand_image=Upload()
        )
        return CreateCategory(status="done")
