from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from graphql_jwt.decorators import jwt_cookie
# from channels.routing import route_pattern_match
# from graphql_ws.django_channels import GraphQLSubscriptionConsumer
from core_marketing.views import getGen
from graphql_playground.views import GraphQLPlaygroundView
from django.views.generic import TemplateView
from django.conf.urls import url


class Home(TemplateView):
    template_name = "index.html"


class GqlView(FileUploadGraphQLView, LoginRequiredMixin):
    pass


urlpatterns = [
    path('admin-core12/', admin.site.urls),
    path('graphql/',  csrf_exempt(jwt_cookie(GqlView.as_view(graphiql=True)))),
    path('rel/<str:plan>/', getGen),
    path('playground/', GraphQLPlaygroundView.as_view(endpoint="/graphql/")),
    #path('', Home.as_view())
    url(r'^(?!admin-core12|graphql|static|media|css|rel|playground|store-p).*$',
        Home.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
