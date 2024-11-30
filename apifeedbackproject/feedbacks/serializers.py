from rest_framework import serializers
from .models import API, Organization, APIStatus
from django.db import models

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'created_at']


class APIStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIStatus
        fields = ['status_code', 'response_time', 'is_available', 'checked_at']


class APISerializer(serializers.ModelSerializer):
    latest_status = serializers.SerializerMethodField()
    metrics = serializers.SerializerMethodField()

    class Meta:
        model = API
        fields = [
            'id', 'name', 'endpoint', 'description', 'is_active',
            'created_at', 'latest_status', 'metrics'
        ]

    def get_latest_status(self, obj):
        latest = obj.status_checks.first()
        if latest:
            return APIStatusSerializer(latest).data
        return None

    def get_metrics(self, obj):
        feedbacks = obj.feedbacks.all()
        return {
            'total_feedback': feedbacks.count(),
            'average_rating': feedbacks.aggregate(models.Avg('rating'))['rating__avg'],
            'average_response_time': feedbacks.aggregate(
                models.Avg('response_time')
            )['response_time__avg']
        }