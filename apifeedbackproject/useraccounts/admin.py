from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

class CustomUserAccountAdmin(UserAdmin):
    # Define the model's fields that you want to display in the admin panel
    model = UserAccount
    list_display = ('email', 'first_name', 'last_name', 'username', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('email',)

    # Define the fields to display when creating or updating a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'contact_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )

    # Define the fields to display in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'contact_number', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Custom method for saving the user model
    def save_model(self, request, obj, form, change):
        obj.save()

# Register the custom admin class with the UserAccount model
admin.site.register(UserAccount, CustomUserAccountAdmin)
