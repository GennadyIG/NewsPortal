from django.urls import path
from .views import (PostList, PostDetail, ArticleCreate, ArticleUpdate, ArticleDelete)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
