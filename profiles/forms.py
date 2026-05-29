"""
FORMULARIOS de la app 'profiles'.

Formularios relacionados con perfiles de usuario y seguimientos.
"""

from django import forms


class ProfileFollow(forms.Form):
    """
    Formulario para alternar seguimiento (un solo botón en la plantilla).

    Solo envía el id del perfil; la vista decide si seguir o dejar de seguir.
    """

    profile_pk = forms.IntegerField(widget=forms.HiddenInput())
