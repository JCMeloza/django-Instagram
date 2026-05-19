from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField('Biografía', max_length=500, blank=True, null=True)
    birth_date = models.DateField('Fecha de nacimiento', blank=True, null=True)
    #followers = models.ManyToManyField(User, symmetrical=False ,related_name='followers',through='Follow')

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'
    
    def __str__(self):
        return self.user.username