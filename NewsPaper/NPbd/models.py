from django.db import models
from .resources import *
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    author_rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return User.objects.get(pk=self.pk).username

    def update_rating(self) -> None:
        summ_rating = 0
        # добавляем суммарный рейтинг постов автора
        user_posts = self.post_set.all()
        summ_rating += user_posts.aggregate(s=models.Sum('post_rating'))['s'] * 3
        # добавляем суммарный рейтинг комментариев автора
        summ_rating += self.author.comment_set.aggregate(s=models.Sum('comment_rating'))['s']
        # добавляем рейтинг коментариев к постам автора, без учета комментариев автора
        summ_rating += Comment.objects.filter(post__in=user_posts).exclude(user__author=self).aggregate(s=models.Sum('comment_rating'))['s']
        self.author_rating = summ_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    category = models.ManyToManyField('Category', through='PostCategory')
    post_type = models.CharField(max_length=2, choices=TYPE_TEXT, default=article)
    adding_time = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.post_title}'

    def get_absolute_url(self):
        if self.post_type == 'NW':
            return reverse('news_detail', args=[str(self.id)])
        else:
            return reverse('article_detail', args=[str(self.id)])

    def like(self) -> None:
        self.post_rating += 1
        self.save()

    def dislike(self) -> None:
        self.post_rating -= 1
        self.save()

    def preview(self) -> str:
        return f'{self.post_text[:123]}...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.category}: {self.post}'


class Comment(models.Model):
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.preview()

    def preview(self) -> str:
        return f'{self.comment_text[:123]}...'

    def like(self) -> None:
        self.comment_rating += 1
        self.save()

    def dislike(self) -> None:
        self.comment_rating -= 1
        self.save()
