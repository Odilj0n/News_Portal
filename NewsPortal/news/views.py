from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView, TemplateView

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category


# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = 'created_at'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['news'] = Post.objects.all()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()

        return context


class PostSearch(ListView):
    model = Post
    ordering = 'created_at'
    template_name = 'news/post_search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',
                           'news.change_post')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',
                           'news.change_post')
    model = Post
    template_name = 'news/post_delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('news.add_post',
                           'news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'news/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'news/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_post_list'

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['post_category'] = self.post_category
        return context


@login_required
@csrf_protect
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей в категории '

    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
