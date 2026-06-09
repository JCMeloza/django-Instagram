"""
VISTAS de la app 'posts'.

Aquí solo está la creación de publicaciones; el listado en home está en instagram/views.py.
"""

from django.http.response import JsonResponse
from django.urls import reverse_lazy,reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib import messages
from posts.models import Post
from .forms import PostCreateForm, CommentCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect


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
class PostDetailView(DetailView, CreateView):
    """
    Detalle del post.
    /post/<int:pk>/ 
    """
    template_name = "posts/post_detail.html"
    model = Post
    context_object_name = 'post'
    form_class = CommentCreateForm

    def form_valid(self, form):
        """
        Antes de guardar, asignamos el autor y el post.
        """
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)

    def get_success_url(self):
        """Tras crear el comentario, volvemos a ver el detalle de post"""
        messages.add_message(self.request, messages.SUCCESS, "Comentario creado correctamente.")
        return reverse('post_detail', args=[self.get_object().pk])

@login_required
def like_post(request,pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        messages.add_message(request, messages.INFO, "Ya no te gusta la publicación")
        post.likes.remove(request.user)
        
    else:
        post.likes.add(request.user)
        messages.add_message(request, messages.INFO, "Te gusta la publicación")

        
    return HttpResponseRedirect(reverse('post_detail', args=[pk]))

@login_required
def like_post_ajax(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
        message = 'Ya no te gusta la publicación'
    else:
        post.likes.add(request.user)
        liked = True
        message = 'Te gusta la publicación'

    return JsonResponse({
        'message': message,
        'liked': liked,
        'likes_count': post.likes.count(),
    })
