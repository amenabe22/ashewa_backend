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

class GqlView(FileUploadGraphQLView, LoginRequiredMixin):
    pass


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/',  csrf_exempt(jwt_cookie(GqlView.as_view(graphiql=True)))),
    path('rel/<str:plan>/', getGen)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
