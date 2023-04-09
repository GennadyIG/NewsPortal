from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from datetime import timedelta
from .models import Post


@shared_task
def weekly_newsletter():
    print('1')
    week = timezone.now() - timedelta(weeks=2)
    posts = Post.objects.filter(adding_time__gt=week)
    if not posts:
        return
    for user in User.objects.all():
        # Список названий категорий-подписок пользователя
        userSub = user.subscriptions.all().values_list('category__name', flat=True)
        user_news = tuple(post for post in posts
                          if set(post.category.all().values_list('name', flat=True)).intersection(set(userSub)))
        if user_news:
            subject = f'Список статей по Вашим подпискам за последнюю неделю'
            text_content = '\n'.join([f'{news.post_title}: '
                                      f'http://127.0.0.1{news.get_absolute_url()}' for news in user_news])
            html_content = '<br><br>'.join([f'<a href="http://127.0.0.1{news.get_absolute_url()}">'
                                            f'{news.post_title}</a><br>{news.preview()}' for news in user_news])
            msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def notify_new_post(post_id):
    print('1')
    post = Post.objects.get(pk=post_id)
    emails = User.objects.filter(
            subscriptions__category__name__in=post.category.all().values_list('name', flat=True)
        ).values_list('email', flat=True)

    postType = {'NW': ('Новость', 'новость'),
                'AR': ('Статья', 'статью')
                }
    subject = f'Новый пост в категории {", ".join(post.category.all().values_list("name", flat=True))}'
    text_content = (
        f'{postType[post.post_type][0]}: {post.post_title}\n'
        f'Превью: {post.preview()}\n\n'
        f'Ссылка на {postType[post.post_type][1]}: http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'{postType[post.post_type][0]}: <b>{post.post_title}</b><br>'
        f'{post.preview()}<br><br>'
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
        f'Ссылка на {postType[post.post_type][1]}</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
