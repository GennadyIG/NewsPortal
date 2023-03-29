from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category.name
    ).values_list('email', flat=True)
    postType = {'NW': ('Новость', 'новость'),
                'AR': ('Статья', 'статью')
                }

    subject = f'Новый пост в категории {instance.category.name}'

    text_content = (
        f'{postType[instance.post_type][0]}: {instance.post_title}\n'
        f'Превью: {instance.preview()}\n\n'
        f'Ссылка на {postType[instance.post_type][1]}: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'{postType[instance.post_type][0]}: {instance.post_title}<br>'
        f'Превью: {instance.preview()}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на {postType[instance.post_type][1]}</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
