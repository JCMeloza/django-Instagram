"""
VISTAS de la app 'posts'.

Aquí solo está la creación de publicaciones; el listado en home está en instagram/views.py.
"""

from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib import messages
from posts.models import Post
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    """
    Formulario para subir un post (/post/create/).

    CreateView + ModelForm crean una fila en la tabla Post al enviar el formulario.
    """

    template_name = "posts/post_create.html"
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Antes de guardar, asignamos el autor.

        form.instance es el objeto Post que se va a insertar; si no ponemos user,
        la base de datos fallaría porque user es obligatorio (ForeignKey).
        """
        form.instance.user = self.request.user

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Publicación creada correctamente.",
        )
        return super(PostCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    """
    Detalle del post.
    /post/<int:pk>/ 
    """
    template_name = "posts/post_detail.html"
    model = Post
    context_object_name = 'post'
