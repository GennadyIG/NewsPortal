from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'id'
    template_name = 'all_news.html'
    context_object_name = 'all_news'
