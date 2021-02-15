from .views import StoreView
from django.urls import path

urlpatterns = [
    path('', StoreView.as_view())
]
