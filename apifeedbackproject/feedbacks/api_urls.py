from django.urls import path
from .api_views import ApiAPIView, FeedbackAPIView

urlpatterns = [
    path('api/', ApiAPIView.as_view(), name='api-list'),
    path('api-feedbacks/', FeedbackAPIView.as_view(), name='api-feedbacks'),
]