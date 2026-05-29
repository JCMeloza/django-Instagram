"""
FORMULARIOS de la app 'instagram'.

Un formulario en Django:
  - Define qué campos ve el usuario (inputs en HTML).
  - Valida los datos (obligatorio, formato email, etc.).
  - Puede guardar en la base de datos (ModelForm) o solo devolver datos limpios (Form).

Los formularios se enlazan con vistas FormView / CreateView / UpdateView.
"""

from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    """
    Formulario de registro: crea un User de Django.

    ModelForm genera campos automáticamente según el modelo User, pero añadimos
  password aparte porque en el modelo User la contraseña se guarda hasheada.
    """

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'first_name',
            'username',
            'email',
            'password',
        ]

    def save(self, commit=True):
        """
        Personalizamos el guardado:

        1. set_password() hashea la contraseña (nunca guardar texto plano).
        2. Creamos UserProfile para que cada usuario tenga datos extra (bio, foto...).

        commit=False en super().save() permite modificar el objeto antes del INSERT.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        from profiles.models import UserProfile
        UserProfile.objects.create(user=user)
        return user


class LoginForm(forms.Form):
    """
    Formulario de login: NO es ModelForm porque no creamos filas nuevas al entrar.

    Solo necesitamos leer username y password y pasarlos a authenticate() en la vista.
    """

    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())


class ProfileFollow(forms.Form):
    """
    Formulario mínimo para el botón 'Seguir'.

    Un solo campo oculto (HiddenInput) con el id del perfil a seguir.
    La plantilla envía profile_pk por POST; la vista lo lee en form_valid().
    """

    profile_pk = forms.IntegerField(widget=forms.HiddenInput())
