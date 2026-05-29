"""
FORMULARIOS de la app 'posts'.
"""

from posts.models import Post
from django import forms


class PostCreateForm(forms.ModelForm):
    """
    Formulario para crear un post: solo imagen y descripción.

    El usuario NO elige el autor en el formulario; la vista asigna request.user
    en form_valid() por seguridad (evita que alguien publique como otro usuario).
    """

    class Meta:
        model = Post
        fields = [
            'image',
            'caption',
        ]
