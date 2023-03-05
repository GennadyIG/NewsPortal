from django.db import models
from .resources import *
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    author_rating = models.IntegerField(default=0)

    def update_rating(self) -> None:
        summ_rating = 0
        # добавляем суммарный рейтинг постов автора
        summ_rating += sum((post.post_rating for post in self.post_set.all())) * 3
        # добавляем суммарный рейтинг комментариев автора
        summ_rating += sum((comment.comment_rating for comment in Comment.objects.filter(user_id=self.pk)))
        # добавляем рейтинг коментариев к постам автора, без учета комментариев автора
        for post in self.post_set.all():
            for comment in post.comment_set():
                if comment.user_id != self.pk:
                    summ_rating += comment.comment_rating

        self.author_rating = summ_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    category = models.ManyToManyField('Category', through='PostCategory')
    post_type = models.CharField(max_length=2, choices=TYPE_TEXT, default=article)
    adding_time = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_title}: {self.preview()}'

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


class Comment(models.Model):
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self) -> None:
        self.comment_rating += 1
        self.save()

    def dislike(self) -> None:
        self.comment_rating -= 1
        self.save()
