from django.urls import path
from .api_views import ApiAPIView

urlpatterns = [
    path('api/', ApiAPIView.as_view(), name='api-list'),
]