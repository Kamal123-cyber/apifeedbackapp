from rest_framework import serializers
from .models import API, Organization, APIStatus, Feedback
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

class FeedbackSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            'id',
            'api',
            'user',
            'user_email',
            'rating',
            'comment',
            'response_time',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None


class APIDetailSerializer(serializers.ModelSerializer):
    recent_status = serializers.SerializerMethodField()
    total_feedbacks = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()

    class Meta:
        model = API
        fields = [
            'id',
            'name',
            'endpoint',
            'description',
            'is_active',
            'created_at',
            'last_checked',
            'organization_name',
            'recent_status',
            'total_feedbacks',
            'average_rating'
        ]

    def get_recent_status(self, obj):
        recent_status = obj.status_checks.first()
        return APIStatusSerializer(recent_status).data if recent_status else None

    def get_total_feedbacks(self, obj):
        return obj.feedbacks.count()

    def get_average_rating(self, obj):
        feedbacks = obj.feedbacks.all()
        return feedbacks.aggregate(models.Avg('rating'))['rating__avg'] or 0

    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None

class APICreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = API
        fields = [
            'name',
            'endpoint',
            'description',
            'organization',
            'is_active'
        ]
        extra_kwargs = {
            'api_key': {'write_only': True}
        }