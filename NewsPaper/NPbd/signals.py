from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, **kwargs):
    emails = User.objects.filter(
        subscriptions__category__name__in=instance.category.all().values_list('name', flat=True)
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
