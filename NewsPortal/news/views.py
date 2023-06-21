from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, DeleteView
from .models import Post


# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['news'] = Post.objects.all()

        return context


class PostDetail(DeleteView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
