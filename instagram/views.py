from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from  django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm, LoginForm
from  django.contrib import messages


# Create your views here.
class HomeView(TemplateView):
    template_name= "general/home.html"

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

