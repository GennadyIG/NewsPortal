import django_filters as filters
from django.utils.translation import gettext_lazy as _
from .models import Category
from django import forms


class PostFilter(filters.FilterSet):
    post_title = filters.CharFilter(field_name='post_title', label=_('Заголовок содержит'), lookup_expr='icontains')
    adding_time = filters.DateFilter(field_name='adding_time', lookup_expr='date__gte', label=_('Дата добавления'),
                                     widget=forms.DateInput(attrs={'type': 'date', 'value': '1970-01-01'}))
    category = filters.ModelChoiceFilter(field_name='category', label=_('Категория'), queryset=Category.objects.all(),
                                         lookup_expr='exact',
                                         empty_label=_('любая'))
