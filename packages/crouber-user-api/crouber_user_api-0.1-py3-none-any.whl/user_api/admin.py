from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from profile_api.models import Profile


class UserProfileInline(admin.StackedInline):
    model = Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    inlines = [UserProfileInline]

    list_display = ("get_full_name", 'email', 'is_superuser', 'is_staff',
                    'is_active', 'last_login', 'created_date', 'modified_date')
    list_filter = ('email', 'firstname', 'lastname', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'firstname', 'lastname', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',
                                    'groups', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff',
                       'is_active')}
         ),
    )
    search_fields = ('email', 'firstname', 'lastname', 'birth_date',
                     'profile_name')
    ordering = ('firstname', 'lastname', 'email',)

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = ("Full name")
