from django import template
from django.contrib.auth.models import Group

from ..models import Post

register = template.Library()

censor_list = ['редиска', 'Редиска']


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError('Попытка применить фильтр не к строковому типу данных')
    for word in censor_list:
        if word in value:
            value = value.replace(word, f'{word[0]}{"*" * (len(word)-1)}')
    return value


# Принадлежность к группе
@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()

@register.filter(name='groups')
def groups(user):
    return user.groups.all()


@register.filter(name='user_posts')
def user_posts(user):
    posts = Post.objects.filter(author__author=user)

    return len(posts)
