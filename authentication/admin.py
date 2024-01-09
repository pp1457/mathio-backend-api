from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile, UserContest

admin.site.register(UserProfile)
admin.site.register(UserContest)

class UserContestInline(admin.StackedInline):
    model = UserContest
    can_delete = False
    verbose_name_plural = 'User Contest'

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    inlines = [UserContestInline, ]

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'user_profile_info')  # Add 'user_profile_info'

    def user_profile_info(self, obj):
        if hasattr(obj, 'profile'):  # Check if UserProfile exists
            profile = obj.profile
            profile_url = f"/admin/authentication/userprofile/{profile.id}/change/"
            return format_html('<a href="{}">profile</a><br/>Rating: {}', profile_url, profile.rating)
        return None

    user_profile_info.short_description = 'UserProfile Information'  # Column header in admin


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
