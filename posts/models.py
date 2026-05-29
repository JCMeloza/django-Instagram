"""
MODELOS de la app 'posts'.

Publicaciones (Post) y comentarios (Comment) del clon de Instagram.
"""

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Una publicación: imagen + texto opcional.

    ForeignKey a User: muchos posts pueden pertenecer a un usuario.
    related_name='posts' → user.posts.all() devuelve sus publicaciones.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Usuario',
    )
    image = models.ImageField('Imagen', upload_to='posts/')
    caption = models.TextField('Descripción', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creacion')

    # Usuarios que han dado like; preparado para funcionalidad futura.
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        verbose_name='Número Likes',
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'


class Comment(models.Model):
    """
    Comentario en un post.

    Dos ForeignKey: a qué post pertenece y qué usuario lo escribió.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Comentario', blank=True, null=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'Comentó {self.user.username} el post {self.post}'
