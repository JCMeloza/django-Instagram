from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from  django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import ProfileFollow, RegistrationForm, LoginForm
from  django.contrib import messages
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Post

# Create your views here.
class HomeView(TemplateView):
    template_name= "general/home.html"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        last_posts = Post.objects.all().order_by('-created_at')[:5]
        context['last_posts'] = last_posts

        return context

class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
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
    def post(self, request):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
        return HttpResponseRedirect(reverse('home'))

    def get(self, request):
        return self.post(request)

            

class RegisterView(CreateView):
    template_name = "general/register.html"
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    def form_valid(self,form):
        messages.add_message(self.request, messages.SUCCESS, "Usuarios creado con exito")
        return super(RegisterView,self).form_valid(form)




class LegalView(TemplateView):
    template_name = "general/legal.html"

class ContactView(TemplateView):
    template_name = "general/contact.html"

@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView, FormView):
    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = 'profile'
    form_class = ProfileFollow

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['profile']
        context['last_posts'] = (
            Post.objects.filter(user=profile.user).order_by('-created_at')
        )
        return context

    def form_valid(self, form):
        profile_pk = form.cleaned_data['profile_pk']
        profile = UserProfile.objects.get(pk=profile_pk)
        self.request.user.profile.follow(profile)
        
        messages.success(self.request, f'Usuario seguido correctamente')
        return super(ProfileDetailView,self).form_valid(form)
    def get_success_url(self):
        return reverse('profile_detail', args=[self.request.user.profile.pk])

@method_decorator(login_required, name='dispatch')
class ProfileListlView(ListView):
    model = UserProfile
    template_name = "general/profile_list.html"
    context_object_name = 'profiles'

    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)

    

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = 'profile'
    fields = ['profile_picture','bio','birth_date']

    def form_valid(self,form):
        messages.add_message(self.request, messages.SUCCESS, "Perfil editado correctamente")
        return super(ProfileUpdateView, self).form_valid(form)
    def get_success_url(self):
        return reverse('profile_detail', args=[self.object.pk])

    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)
    
