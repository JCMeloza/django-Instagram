"""
Panel de administración para posts y comentarios.
"""

from django.contrib import admin
from posts.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Lista de publicaciones en /admin/."""

    list_display = ('user', 'created_at', 'caption')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Lista de comentarios en /admin/."""

    list_display = ('user', 'created_at', 'text')
