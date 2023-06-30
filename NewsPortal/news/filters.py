import django_filters
from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter

from django import forms
from .models import Post, Category, PostCategory, Author


class PostFilter(FilterSet):
    created_at = DateTimeFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gt',
        label='Непозднее'
    )
    post_PostCategory = ModelChoiceFilter(
        field_name='post_category__category_name',
        queryset=Category.objects.all(),
        label='Категория',
    )

    author = django_filters.ModelChoiceFilter(field_name='author',
                                              label='Выбор автора',
                                              lookup_expr='exact',
                                              queryset=Author.objects.all())

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
        }
