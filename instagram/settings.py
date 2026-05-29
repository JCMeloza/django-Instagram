"""
CONFIGURACIÓN global del proyecto Django.

Este archivo se carga al arrancar el servidor (manage.py runserver).
Define apps instaladas, base de datos, plantillas, idioma, archivos media, etc.
"""

from pathlib import Path
from django.urls import reverse_lazy

# Carpeta raíz del proyecto (donde está manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta donde están las plantillas HTML del proyecto.
TEMPLATES_DIR = BASE_DIR / "instagram" / "templates"

# Clave secreta: firma cookies y sesiones. En producción debe ser privada y distinta.
SECRET_KEY = 'django-insecure-66&rc-hk*ka789v@0l&-_qll%781yi@v2z6d4))drg@$)uen(4'

# True = muestra errores detallados; NUNCA dejar True en producción pública.
DEBUG = True

# Dominios permitidos para servir la app (vacío = solo desarrollo local).
ALLOWED_HOSTS = []

# Aplicaciones instaladas: Django trae las de contrib y nosotros añadimos las nuestras.
INSTALLED_APPS = [
    'django.contrib.admin',      # Panel /admin/
    'django.contrib.auth',       # Usuarios, login, permisos
    'django.contrib.contenttypes',
    'django.contrib.sessions',     # Sesiones (quién está logueado)
    'django.contrib.messages',   # Mensajes flash (messages.success, etc.)
    'django.contrib.staticfiles',  # CSS/JS estáticos

    'django_extensions',   # Comandos extra de desarrollo
    'crispy_forms',          # Formularios bonitos en plantillas
    'crispy_bootstrap5',

    'profiles',        # Perfiles y seguidores
    'posts',           # Publicaciones y comentarios
    'notifications',   # Reservada para el futuro
]

# Middleware: capas que procesan cada petición (seguridad, sesión, CSRF...).
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Protege formularios POST
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # request.user
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Módulo principal de URLs (instagram/urls.py).
ROOT_URLCONF = 'instagram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],  # Plantillas del proyecto
        'APP_DIRS': True,         # También busca templates/ dentro de cada app
        'OPTIONS': {
            'context_processors': [
                # Variables disponibles en TODAS las plantillas:
                'django.template.context_processors.request',  # request
                'django.contrib.auth.context_processors.auth',  # user, perms
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'instagram.wsgi.application'

# Base de datos SQLite: un archivo db.sqlite3 en la raíz (ideal para aprender).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Reglas de contraseñas al registrarse.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS del CDN Bootstrap va por enlace en layout.html).
STATIC_URL = 'static/'

# Archivos subidos por usuarios (fotos de perfil y posts).
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# django-crispy-forms usará estilos Bootstrap 5.
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Si un usuario no logueado entra en una vista @login_required, va aquí.
LOGIN_URL = reverse_lazy('login')
