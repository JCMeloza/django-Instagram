# Guía de aprendizaje — Clon Instagram (Django)

Documento para **principiantes**. El código Python tiene comentarios línea a línea en cada función.

## ¿Cómo funciona una petición?

```
Usuario → URL (urls.py) → Vista (views.py) → Modelo (models.py) / Formulario (forms.py) → Plantilla HTML
```

## Estructura del proyecto

| Carpeta / archivo | Para qué sirve |
|-------------------|----------------|
| `manage.py` | Comandos: servidor, migraciones, admin |
| `instagram/settings.py` | Configuración global |
| `instagram/urls.py` | Mapa URL → vista |
| `instagram/views.py` | Home, login, perfiles, registro |
| `instagram/forms.py` | Formularios de registro, login, seguir |
| `instagram/templates/` | HTML que ve el usuario |
| `profiles/models.py` | UserProfile, Follow |
| `posts/models.py` | Post, Comment |
| `posts/views.py` | Crear publicación |
| `db.sqlite3` | Base de datos (se crea con migrate) |
| `media/` | Fotos subidas por usuarios |

## URLs principales

| URL | Vista | Qué hace |
|-----|-------|----------|
| `/` | HomeView | Últimos 5 posts |
| `/login/` | LoginView | Iniciar sesión |
| `/register/` | RegisterView | Crear cuenta + perfil |
| `/profile/list/` | ProfileListlView | Ver otros usuarios |
| `/profile/3/` | ProfileDetailView | Ver perfil y seguir |
| `/profile/update/3/` | ProfileUpdateView | Editar tu perfil |
| `/post/create/` | PostCreateView | Subir foto |

## Plantillas importantes

- `general/layout.html` — Esqueleto (Bootstrap, cabecera, pie).
- `general/home.html` — Incluye `_includes/posts/_posts.html` en bucle.
- `general/profile_detail.html` — Datos del perfil + botón Seguir.
- `_includes/_header.html` — Menú según estés logueado o no.

## Conceptos que practicas en este proyecto

1. **Modelos** — Tablas y relaciones (ForeignKey, OneToOne, ManyToMany).
2. **Migraciones** — `makemigrations` + `migrate`.
3. **Vistas genéricas** — TemplateView, ListView, DetailView, CreateView, FormView.
4. **Autenticación** — `login`, `logout`, `@login_required`.
5. **Formularios** — ModelForm, validación, `form_valid`.
6. **Plantillas** — `{% extends %}`, `{% for %}`, `{% url %}`, `{% csrf_token %}`.
7. **Archivos media** — ImageField y `MEDIA_URL`.

## Orden recomendado para estudiar el código

1. `profiles/models.py` y `posts/models.py`
2. `instagram/urls.py`
3. `instagram/forms.py`
4. `instagram/views.py` (empezar por HomeView y LoginView)
5. `posts/views.py`
6. Plantillas empezando por `layout.html` y `home.html`

## App `notifications`

Instalada pero vacía: pensada para avisos de “te ha seguido X” en el futuro.
