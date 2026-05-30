"""
RUTAS (URLs) del proyecto.

Cada path() dice: 'si la URL coincide, ejecuta esta vista'.
El parámetro name='...' permite generar enlaces en plantillas: {% url 'home' %}.

Orden importante: rutas más específicas (profile/list/) ANTES que genéricas (profile/<pk>/).
"""

from django.contrib import admin
from django.urls import path
from .views import (
    HomeView,
    LoginView,
    LogoutView,
    ProfileUpdateView,
    RegisterView,
    LegalView,
    ContactView,
    ProfileDetailView,
    ProfileListView,
)
from django.conf.urls.static import static
from django.conf import settings
from posts.views import PostCreateView, PostDetailView

urlpatterns = [
    # Página principal: feed con últimas publicaciones.
    path('', HomeView.as_view(), name='home'),

    # Autenticación: entrar, salir y registrarse.
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # Perfiles: listado, detalle (ver + seguir) y edición del propio perfil.
    path('profile/list/', ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='profile_update'),

    # Crear una publicación con imagen (app posts).
    path('post/create/', PostCreateView.as_view(), name='post_create'),

    # Páginas informativas estáticas.
    path('legal/', LegalView.as_view(), name='legal'),
    path('contact/', ContactView.as_view(), name='contact'),

    #Página para detalle de un post
    path('popsts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Panel de administración de Django (superusuario).
    path('admin/', admin.site.urls),
]

# En desarrollo: servir archivos subidos (fotos) desde la carpeta media/.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
