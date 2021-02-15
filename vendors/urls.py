from .views import StoreView
from django.urls import path

url_patterns = [
    path('store-p/', StoreView.as_view())
]
