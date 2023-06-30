from datetime import datetime

from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from .filters import PostFilter
from .forms import PostForm
from .models import Post


# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = 'created_at'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['news'] = Post.objects.all()

        return context


class PostSearch(ListView):
    model = Post
    ordering = 'created_at'
    template_name = 'news/post_search.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DeleteView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/create/':
                post.post_type = Post.TYPES[1]
                # Post.POSTS = ['article', 'news_piece']
            elif path_info == '/article/create/':
                post.post_type = Post.TYPES[0]
                # Post.POSTS = ['article', 'news_piece']
            else:
                raise ValidationError(
                    'PostCreate.from_valid(): Wrong url.'
                )

        post.save()
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('post_list')


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_edit.html'
