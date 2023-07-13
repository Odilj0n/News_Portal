from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),

    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),

    path('upgrade/', upgrade_me, name='upgrade'),

    path('profile/', Profile.as_view(), name= 'profile'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')


]
