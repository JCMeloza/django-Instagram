from django.contrib import admin
from .models import UserProfile , Follow

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date')
    list_filter = ('birth_date',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower','following','created_at')
    list_filter = ('created_at',)