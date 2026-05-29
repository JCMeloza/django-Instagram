"""
Panel de administración (/admin/) para modelos de 'profiles'.

register() hace que los modelos aparezcan en el admin de Django.
list_display / list_filter mejoran la lista de registros.
"""

from django.contrib import admin
from .models import UserProfile, Follow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Configuración de cómo se listan los perfiles en el admin."""

    list_display = ('user', 'birth_date')
    list_filter = ('birth_date',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Configuración de la tabla de seguimientos en el admin."""

    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
