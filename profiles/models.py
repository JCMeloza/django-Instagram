"""
MODELOS de la app 'profiles'.

Un modelo = una tabla en la base de datos + métodos Python para trabajar con ella.
Django crea las tablas al ejecutar: python manage.py migrate
"""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Perfil extendido ligado 1 a 1 con User (auth de Django).

    User guarda login; UserProfile guarda bio, foto, seguidores, etc.
    related_name='profile' → desde user accedemos: request.user.profile
    """

    # CASCADE: si se borra el User, se borra su UserProfile.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    profile_picture = models.ImageField(
        'Imagen de perfil',
        upload_to='profile_pictures/',
        blank=True,
        null=True,
    )
    bio = models.TextField('Biografía', max_length=500, blank=True, null=True)
    birth_date = models.DateField('Fecha de nacimiento', blank=True, null=True)

    # Relación "me sigue / sigo a" entre perfiles, con tabla intermedia Follow.
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        through='Follow',
    )

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'

    def __str__(self):
        """Texto que aparece en el admin y al imprimir el objeto."""
        return self.user.username

    def follow(self, profile):
        """
        Hace que ESTE perfil siga a otro.

        get_or_create evita duplicados si pulsas 'Seguir' dos veces.
        follower = quien sigue (self); following = a quién se sigue (profile).
        """
        Follow.objects.get_or_create(follower=self, following=profile)


class Follow(models.Model):
    """
    Tabla intermedia: una fila = una relación de seguimiento.

    Usamos modelo explícito (en lugar de solo M2M) para guardar created_at
    y poder ampliar luego (notificaciones, etc.).
    """

    follower = models.ForeignKey(
        UserProfile,
        verbose_name='¿Quien sigue?',
        on_delete=models.CASCADE,
        related_name='follower_set',
    )
    following = models.ForeignKey(
        UserProfile,
        verbose_name='¿A quien sigue?',
        on_delete=models.CASCADE,
        related_name='following_set',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='¿Desde cuando le sigue?',
    )

    class Meta:
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'
        # Un usuario no puede seguir dos veces al mismo perfil.
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'
