from django.contrib import admin
from .models import Organization, OrganizationMember, API, APIStatus, Feedback

# Admin for Organization model
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # Fields to display in list view
    search_fields = ('name',)  # Add search functionality
    ordering = ('-created_at',)  # Default ordering by created_at (descending)

# Admin for OrganizationMember model
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('organization', 'user', 'role', 'joined_at')  # Fields to display in list view
    list_filter = ('role', 'organization')  # Filter by role and organization
    search_fields = ('user__username', 'organization__name')  # Add search functionality based on user and organization

# Admin for API model
class APIAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'endpoint', 'is_active', 'created_at')  # Fields to display
    list_filter = ('is_active', 'organization')  # Filter by active status and organization
    search_fields = ('name', 'organization__name', 'endpoint')  # Search by name, organization, and endpoint
    ordering = ('-created_at',)  # Default ordering by created_at (descending)

# Admin for APIStatus model
class APIStatusAdmin(admin.ModelAdmin):
    list_display = ('api', 'status_code', 'response_time', 'is_available', 'checked_at')  # Fields to display
    list_filter = ('is_available', 'api')  # Filter by availability and API
    search_fields = ('api__name',)  # Search by API name
    ordering = ('-checked_at',)  # Default ordering by checked_at (descending)

# Admin for Feedback model
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('api', 'user', 'rating', 'response_time', 'created_at')  # Fields to display
    list_filter = ('rating', 'api')  # Filter by rating and API
    search_fields = ('user__username', 'api__name')  # Search by user and API name
    ordering = ('-created_at',)  # Default ordering by created_at (descending)

# Register models with the admin site
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationMember, OrganizationMemberAdmin)
admin.site.register(API, APIAdmin)
admin.site.register(APIStatus, APIStatusAdmin)
admin.site.register(Feedback, FeedbackAdmin)