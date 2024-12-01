from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import API, APIStatus, Feedback
from django.utils import timezone
import requests
from django.db.models import Avg
from .serializers import APIStatusSerializer, APISerializer, FeedbackSerializer

# API View to list all APIs
class ApiAPIView(APIView):
    def get(self, request):
        api_obj = API.objects.all()
        serializer = APISerializer(api_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API View to check the status of a specific API
class APIStatusCheckAPIView(APIView):
    def post(self, request, id):
        try:
            api = API.objects.get(id=id)
            start_time = timezone.now()
            response = requests.get(api.endpoint, timeout=5)
            end_time = timezone.now()
            response_time = (end_time - start_time).total_seconds()

            # Create APIStatus record
            status_check = APIStatus.objects.create(
                api=api,
                status_code=response.status_code,
                response_time=response_time,
                is_available=response.status_code < 400
            )

            api.last_checked = timezone.now()
            api.save()

            return Response(APIStatusSerializer(status_check).data)

        except requests.RequestException as e:
            api = API.objects.get(id=id)
            status_check = APIStatus.objects.create(
                api=api,
                status_code=0,
                response_time=0,
                is_available=False
            )
            return Response(
                APIStatusSerializer(status_check).data,
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

# API View to get the analytics for a specific API
class APIAnalyticsAPIView(APIView):
    def get(self, request, id):
        try:
            # Fetching the API instance
            api = API.objects.get(id=id)
            feedbacks = api.feedbacks.all()

            # Time-based analysis
            now = timezone.now()
            last_24h = feedbacks.filter(created_at__gte=now - timezone.timedelta(days=1))
            last_7d = feedbacks.filter(created_at__gte=now - timezone.timedelta(days=7))

            # Calculating overall statistics
            overall_average_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']
            overall_average_response_time = feedbacks.aggregate(Avg('response_time'))['response_time__avg']

            # Calculating ratings distribution (1-5)
            ratings_distribution = {
                rating: feedbacks.filter(rating=rating).count() for rating in range(1, 6)
            }

            # Availability calculation for uptime in the last 24 hours
            status_checks_last_24h = api.status_checks.filter(
                checked_at__gte=now - timezone.timedelta(days=1)
            )
            uptime_24h = (
                status_checks_last_24h.filter(is_available=True).count() /
                max(status_checks_last_24h.count(), 1)
            ) * 100 if status_checks_last_24h.count() > 0 else 0

            # Getting the most recent status
            recent_status = APIStatusSerializer(api.status_checks.first()).data if api.status_checks.exists() else None

            return Response({
                'overall': {
                    'total_feedback': feedbacks.count(),
                    'average_rating': overall_average_rating,
                    'average_response_time': overall_average_response_time,
                },
                'last_24h': {
                    'total_feedback': last_24h.count(),
                    'average_rating': last_24h.aggregate(Avg('rating'))['rating__avg'],
                },
                'last_7d': {
                    'total_feedback': last_7d.count(),
                    'average_rating': last_7d.aggregate(Avg('rating'))['rating__avg'],
                },
                'ratings_distribution': ratings_distribution,
                'availability': {
                    'uptime_24h': uptime_24h,
                    'recent_status': recent_status,
                }
            })

        except API.DoesNotExist:
            return Response({'detail': 'API not found'}, status=status.HTTP_404_NOT_FOUND)

class FeedbackAPIView(APIView):
    def get(self, request):
        try:
            feed_obj = Feedback.objects.all()
            feed_serializer = FeedbackSerializer(feed_obj, many=True)
            return Response(feed_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Errors'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)