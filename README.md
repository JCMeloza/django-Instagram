# django-Instagram

Clon educativo de **Instagram** desarrollado con **Django**. Permite registrarse, publicar imágenes, seguir usuarios, dar likes con AJAX y comentar publicaciones. Pensado para aprender vistas genéricas, autenticación, modelos relacionales y plantillas en Django.

---

## Tabla de contenidos

- [Características](#características)
- [Stack tecnológico](#stack-tecnológico)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Uso de la aplicación](#uso-de-la-aplicación)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Rutas principales](#rutas-principales)
- [Modelos de datos](#modelos-de-datos)
- [Panel de administración](#panel-de-administración)
- [Archivos media](#archivos-media)
- [Documentación adicional](#documentación-adicional)
- [Notas de desarrollo](#notas-de-desarrollo)

---

## Características

| Módulo | Funcionalidad |
|--------|----------------|
| **Autenticación** | Registro, login, logout y sesiones de usuario |
| **Perfiles** | Foto, biografía, fecha de nacimiento, edición del perfil propio |
| **Seguimiento** | Seguir / dejar de seguir usuarios, contadores de seguidores y seguidos |
| **Publicaciones** | Crear posts con imagen y descripción |
| **Feed** | Inicio con posts de usuarios seguidos (logueado) o últimas 5 publicaciones (invitado) |
| **Likes** | Me gusta en feed y detalle del post vía AJAX (sin recargar la página) |
| **Comentarios** | Añadir y listar comentarios en el detalle de cada post |
| **Admin** | Gestión de usuarios, perfiles, posts, comentarios y seguimientos |

---

## Stack tecnológico

- **Python 3.10+**
- **Django 5.2**
- **SQLite** (base de datos por defecto)
- **Pillow** — procesamiento de imágenes (`ImageField`)
- **django-crispy-forms** + **crispy-bootstrap5** — formularios con Bootstrap 5
- **django-extensions** — utilidades de desarrollo
- **Bootstrap 5** y **Bootstrap Icons** (CDN en plantillas)

---

## Requisitos previos

- Python 3.10 o superior
- `pip` y `venv`
- Git (opcional, para clonar el repositorio)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd django-Instagram
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

Crea las tablas en la base de datos SQLite (`db.sqlite3`):

```bash
python manage.py migrate
```

### 5. (Opcional) Crear superusuario para el admin

```bash
python manage.py createsuperuser
```

---

## Ejecución

Arrancar el servidor de desarrollo:

```bash
python manage.py runserver
```

Abrir en el navegador:

**http://127.0.0.1:8000/**

Puerto alternativo:

```bash
python manage.py runserver 8001
```

> El servidor de desarrollo de Django **no** está pensado para producción.

---

## Uso de la aplicación

1. **Registrarse** en `/register/` — se crea un `User` y su `UserProfile` automáticamente.
2. **Iniciar sesión** en `/login/`.
3. **Editar perfil** desde *Mi Perfil* → *Editar* (`/profile/update/<id>/`).
4. **Explorar usuarios** en *Perfiles de Usuario* y pulsar *Seguir* o *Dejar de seguir*.
5. **Publicar** en *Publicar* (`/post/create/`).
6. En el **inicio**, si estás logueado verás posts de los usuarios que sigues.
7. En cada post, **Ver Post** abre el detalle: likes (corazón) y comentarios.

---

## Estructura del proyecto

```
django-Instagram/
├── manage.py                 # Punto de entrada (runserver, migrate, etc.)
├── requirements.txt          # Dependencias Python
├── db.sqlite3                # Base de datos (se genera con migrate)
├── media/                    # Imágenes subidas (posts, avatares)
├── GUIA_APRENDIZAJE.md       # Guía didáctica del código
│
├── instagram/                # Proyecto Django (configuración y vistas principales)
│   ├── settings.py           # Configuración global
│   ├── urls.py               # Enrutado de URLs
│   ├── views.py              # Home, auth, perfiles
│   ├── forms.py              # Registro y login
│   ├── wsgi.py / asgi.py
│   └── templates/
│       ├── general/          # layout, home, login, perfiles...
│       ├── posts/            # crear post, detalle post
│       └── _includes/        # header, footer, posts parciales, mensajes
│
├── profiles/                 # App de perfiles y seguimientos
│   ├── models.py             # UserProfile, Follow
│   ├── forms.py              # ProfileFollow (seguir / dejar de seguir)
│   ├── admin.py
│   └── migrations/
│
├── posts/                    # App de publicaciones
│   ├── models.py             # Post, Comment
│   ├── views.py              # Crear post, detalle, likes AJAX
│   ├── forms.py              # PostCreateForm, CommentCreateForm
│   ├── admin.py
│   └── migrations/
│
└── notifications/            # App reservada (notificaciones futuras)
```

### Responsabilidad de cada app

| App | Rol |
|-----|-----|
| `instagram` | Configuración, URLs globales, autenticación, home y vistas de perfil |
| `profiles` | Datos extendidos del usuario y relaciones de seguimiento |
| `posts` | Publicaciones, comentarios y sistema de likes |
| `notifications` | Placeholder para avisos (likes, nuevos seguidores, etc.) |

---

## Rutas principales

| URL | Nombre | Descripción |
|-----|--------|-------------|
| `/` | `home` | Feed de publicaciones |
| `/login/` | `login` | Inicio de sesión |
| `/logout/` | `logout` | Cerrar sesión |
| `/register/` | `register` | Registro de usuario |
| `/profile/list/` | `profile_list` | Listado de otros perfiles |
| `/profile/<id>/` | `profile_detail` | Perfil de un usuario |
| `/profile/update/<id>/` | `profile_update` | Editar perfil propio |
| `/post/create/` | `post_create` | Nueva publicación |
| `/post/<id>/` | `post_detail` | Detalle, likes y comentarios |
| `/post/like-ajax/<id>/` | `post_like_ajax` | API JSON para likes (AJAX) |
| `/legal/` | `legal` | Aviso legal |
| `/contact/` | `contact` | Contacto |
| `/admin/` | — | Panel de administración Django |

---

## Modelos de datos

```
User (Django auth)
 └── UserProfile (1:1) — bio, foto, fecha nacimiento
      └── Follow — follower → following (seguidores)

User
 └── Post (1:N) — imagen, caption, likes (M2M User)
      └── Comment (1:N) — texto, autor, fecha
```

---

## Panel de administración

Tras crear un superusuario:

**http://127.0.0.1:8000/admin/**

Desde ahí puedes gestionar usuarios, perfiles, publicaciones, comentarios y relaciones de seguimiento.

---

## Archivos media

Las imágenes se guardan en:

- `media/profile_pictures/` — avatares
- `media/posts/` — imágenes de publicaciones

En desarrollo, Django sirve `/media/` automáticamente gracias a la configuración en `instagram/urls.py`. En producción hay que configurar el servidor web (Nginx, Apache, etc.) o un almacenamiento en la nube.

---

## Documentación adicional

- **[GUIA_APRENDIZAJE.md](GUIA_APRENDIZAJE.md)** — explicación del flujo Django, orden de estudio del código y conceptos para principiantes.
- Comentarios en el código — las vistas, modelos y formularios incluyen documentación en español.

---

## Notas de desarrollo

### Comandos útiles

```bash
# Crear migraciones tras cambiar modelos
python manage.py makemigrations
python manage.py migrate

# Comprobar el proyecto
python manage.py check

# Shell interactivo de Django
python manage.py shell
```

### Variables de configuración relevantes (`instagram/settings.py`)

| Setting | Valor | Descripción |
|---------|-------|-------------|
| `DEBUG` | `True` | Modo desarrollo (cambiar en producción) |
| `LANGUAGE_CODE` | `es-ES` | Idioma de la interfaz |
| `MEDIA_ROOT` | `media/` | Carpeta de subidas |
| `LOGIN_URL` | `/login/` | Redirección si no hay sesión |

### Likes AJAX

El JavaScript global en `instagram/templates/general/layout.html` intercepta clics en enlaces con clase `.likeButton` y llama a `/post/like-ajax/<id>/`. Los partials de posts y el detalle deben usar esa estructura HTML.

### Producción

Antes de desplegar:

- `DEBUG = False`
- Definir `SECRET_KEY` y `ALLOWED_HOSTS` de forma segura
- Usar PostgreSQL u otro motor en lugar de SQLite si procede
- Configurar `STATIC_ROOT` y servir estáticos/media correctamente

---

## Autor

Proyecto educativo de clon de Instagram con Django.
