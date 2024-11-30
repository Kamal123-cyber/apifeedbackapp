from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='OrganizationMember')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"


class OrganizationMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Organization Member"
        verbose_name_plural = "Organization Members"


class API(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    endpoint = models.URLField()
    description = models.TextField()
    api_key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-created_at']

    class Meta:
        verbose_name = "API"
        verbose_name_plural = "APIs"
        ordering = ['-created_at']


class APIStatus(models.Model):
    api = models.ForeignKey(API, on_delete=models.CASCADE, related_name='status_checks')
    status_code = models.IntegerField()
    response_time = models.FloatField()
    is_available = models.BooleanField()
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "API Status"
        verbose_name_plural = "API Statuses"
        ordering = ['-checked_at']




class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api = models.ForeignKey(API, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    response_time = models.FloatField(help_text="API response time in seconds")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        unique_together = ['api', 'user']
        ordering = ['-created_at']