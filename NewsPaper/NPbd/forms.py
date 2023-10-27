from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'post_title',
            'post_text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("post_title")
        if title.islower():
            raise ValidationError(
                "Заголовок должен начинаться с прописной буквы."
            )
        return cleaned_data
