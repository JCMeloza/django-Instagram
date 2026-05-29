"""
VISTAS del proyecto principal (app 'instagram').

En Django, una 'vista' decide qué respuesta devolver cuando el usuario visita una URL.
Aquí usamos sobre todo VISTAS BASADAS EN CLASES (CBV): cada clase hereda de una vista
genérica de Django (TemplateView, FormView, etc.) y reutiliza lógica común.

Flujo típico:
  1. El usuario pide una URL (ej. /login/)
  2. urls.py enlaza esa URL con una vista (ej. LoginView)
  3. La vista procesa la petición GET o POST y devuelve HTML o una redirección
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm, LoginForm
from profiles.forms import ProfileFollow
from django.contrib import messages
from profiles.models import Follow, UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Post


class HomeView(TemplateView):
    """
    Página de inicio (/).

    TemplateView solo muestra una plantilla HTML; no necesita modelo.
    """

    template_name = "general/home.html"

    def get_context_data(self, **kwargs):
        """
        Añade variables extra que la plantilla puede usar con {{ nombre }}.

        Por qué existe: TemplateView por defecto solo pasa datos básicos;
        nosotros queremos enviar los últimos posts al home.html.
        """
        context = super().get_context_data(**kwargs)

        # Consulta a la base de datos: todos los posts, más nuevos primero, máximo 5.
        last_posts = Post.objects.all().order_by('-created_at')[:5]
        context['last_posts'] = last_posts

        return context


class LoginView(FormView):
    """
    Pantalla de inicio de sesión (/login/).

    FormView muestra un formulario (GET) y lo valida cuando el usuario envía (POST).
    No guarda un modelo directamente: usamos LoginForm (campos sueltos, no ModelForm).
    """

    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        """
        Se ejecuta cuando el formulario es válido (campos rellenados correctamente).

        Aquí comprobamos usuario/contraseña con authenticate() y, si son correctos,
        creamos la sesión con login() para que Django recuerde quién está conectado.
        """
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Bienvenido de nuevo, {user.username}')
            return HttpResponseRedirect(reverse('home'))

        messages.error(self.request, 'Usuario o contraseña no válidos')
        return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    """
    Cierra la sesión del usuario (/logout/).

    @login_required obliga a estar logueado antes de entrar en la vista.
    method_decorator adapta ese decorador de función a una clase (name='dispatch').
    """

    def post(self, request):
        """
        POST: forma recomendada de cerrar sesión (evita que un enlace GET cierre sesión por error).
        """
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
        return HttpResponseRedirect(reverse('home'))

    def get(self, request):
        """
        Si alguien entra por GET, reutilizamos la misma lógica que POST por comodidad.
        """
        return self.post(request)


class RegisterView(CreateView):
    """
    Registro de nuevos usuarios (/register/).

    CreateView crea un objeto en la base de datos a partir de un ModelForm.
    model = User usa la tabla de usuarios que trae Django (auth_user).
    """

    template_name = "general/register.html"
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    def form_valid(self, form):
        """
        Tras guardar el usuario, mostramos un mensaje flash y redirigimos al login.
        El perfil UserProfile se crea dentro de RegistrationForm.save().
        """
        messages.add_message(self.request, messages.SUCCESS, "Usuarios creado con exito")
        return super(RegisterView, self).form_valid(form)


class LegalView(TemplateView):
    """Página estática de aviso legal (/legal/). Solo renderiza la plantilla."""

    template_name = "general/legal.html"


class ContactView(TemplateView):
    """Página estática de contacto (/contact/). Solo renderiza la plantilla."""

    template_name = "general/contact.html"


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView, FormView):
    """
    Detalle de un perfil (/profile/<pk>/) + botón 'Seguir' (POST).

    DetailView: muestra UN objeto (UserProfile) según el pk de la URL.
    FormView: procesa el formulario ProfileFollow al hacer POST.

    Heredamos de ambas porque en la misma página vemos el perfil y enviamos el formulario.
    """

    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = 'profile'  # En la plantilla usamos {{ profile }}, no {{ userprofile }}
    form_class = ProfileFollow

    def get_context_data(self, **kwargs):
        """
        Prepara todos los datos que profile_detail.html necesita.

        self.object / context['profile'] = perfil que estamos viendo (pk de la URL).
        """
        context = super().get_context_data(**kwargs)
        profile = context['profile']

        # Posts publicados por el usuario dueño de este perfil.
        context['last_posts'] = (
            Post.objects.filter(user=profile.user).order_by('-created_at')
        )

        # Tabla Follow: 'following' = perfil que recibe el seguimiento (seguidores de este perfil).
        context['followers_count'] = profile.following_set.count()

        # Tabla Follow: 'follower' = perfil que inicia el seguimiento (a quién sigue este perfil).
        context['following_count'] = profile.follower_set.count()

        # Si True, la plantilla muestra "Dejar de seguir"; si False, "Seguir".
        context['is_following'] = self._is_following(profile)

        return context

    def _is_following(self, profile):
        """Comprueba si el usuario logueado sigue al perfil indicado."""
        return Follow.objects.filter(
            follower=self.request.user.profile,
            following=profile,
        ).exists()

    def form_valid(self, form):
        """
        Un solo POST: si ya lo sigues → unfollow; si no → follow.
        La plantilla solo cambia el texto del botón según is_following.
        """
        profile = UserProfile.objects.get(pk=form.cleaned_data['profile_pk'])
        self.followed_profile_pk = profile.pk

        if self._is_following(profile):
            self.request.user.profile.unfollow(profile)
            messages.success(self.request, 'Has dejado de seguir a este usuario')
        else:
            self.request.user.profile.follow(profile)
            messages.success(self.request, 'Usuario seguido correctamente')

        return super().form_valid(form)

    def get_success_url(self):
        """
        URL de redirección tras un POST correcto (FormView la llama después de form_valid).

        Importante: volvemos al perfil que seguimos, no al nuestro.
        """
        pk = getattr(self, 'followed_profile_pk', self.kwargs['pk'])
        return reverse('profile_detail', args=[pk])


@method_decorator(login_required, name='dispatch')
class ProfileListlView(ListView):
    """
    Lista de perfiles de otros usuarios (/profile/list/).

    ListView muestra muchos objetos del modelo en bucle ({% for profile in profiles %}).
    """

    model = UserProfile
    template_name = "general/profile_list.html"
    context_object_name = 'profiles'

    def get_queryset(self):
        """
        Define QUÉ filas de la base de datos se listan.

        Excluimos nuestro propio perfil para no mostrarnos en 'otros usuarios'.
        """
        return UserProfile.objects.all().exclude(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    """
    Editar mi perfil (/profile/update/<pk>/).

    UpdateView muestra un formulario con los datos actuales y guarda los cambios (POST).
    """

    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = 'profile'
    fields = ['profile_picture', 'bio', 'birth_date']

    def form_valid(self, form):
        """Mensaje de éxito y delegamos el guardado en la base de datos a UpdateView."""
        messages.add_message(self.request, messages.SUCCESS, "Perfil editado correctamente")
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        """Tras editar, volvemos a ver el detalle del mismo perfil."""
        return reverse('profile_detail', args=[self.object.pk])

    def dispatch(self, request, *args, **kwargs):
        """
        Se ejecuta ANTES que get/post: comprobación de seguridad.

        Solo el dueño del perfil puede editarlo; si no, redirigimos al home.
        """
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)
