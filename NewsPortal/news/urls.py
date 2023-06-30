from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostSearch, PostDelete, PostUpdate

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),

    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('article/<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
]

