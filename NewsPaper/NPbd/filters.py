from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Post, Category
from django import forms


class PostFilter(FilterSet):
    adding_time = DateFilter(field_name='adding_time', lookup_expr='date__gte',
                                            widget=forms.DateTimeInput(attrs={'type': 'date'}))
    category = ModelChoiceFilter(field_name='category', queryset=Category.objects.all(), lookup_expr='exact', empty_label='любая')

    class Meta:
        model = Post
        fields = {
            # поиск по названию
            'post_title': ['icontains'],
        }
