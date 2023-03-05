from django import template

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
