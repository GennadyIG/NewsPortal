from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Author
from django.core.cache import cache
from django.utils import timezone
import pytz
from django.shortcuts import redirect
from rest_framework import generics
from .serializers import *


class PostList(ListView):
    model = Post
    ordering = '-adding_time'
    template_name = 'all_news.html'
    context_object_name = 'all_news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | {
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones,
        }
        context['filterset'] = self.filterset
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | {
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones,
        }
        return context

    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(f'{self.kwargs["pk"]}')


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NPbd.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.post_type = 'NW'
        instance.author = Author.objects.get(pk=self.request.user.id)
        instance.save()

        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NPbd.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.post_type = 'AR'
        instance.author = Author.objects.get(pk=self.request.user.id)
        instance.save()

        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NPbd.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.author.id != self.request.user.id and not self.request.user.groups.filter(pk=3).exists():
            raise Http404("Вы не являетесь автором данной новости")
        return super(NewsUpdate, self).dispatch(request, *args, **kwargs)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NPbd.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.author.id != self.request.user.id and not self.request.user.groups.filter(pk=3).exists():
            raise Http404("Вы не являетесь автором данной статьи")
        return super(ArticleUpdate, self).dispatch(request, *args, **kwargs)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NPbd.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.author.id != self.request.user.id and not self.request.user.groups.filter(pk=3).exists():
            raise Http404("Вы не являетесь автором данной новости")
        return super(NewsDelete, self).dispatch(request, *args, **kwargs)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NPbd.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.author.id != self.request.user.id and not self.request.user.groups.filter(pk=3).exists():
            raise Http404("Вы не являетесь автором данной статьи")
        return super(ArticleDelete, self).dispatch(request, *args, **kwargs)

class PostViewSet(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
