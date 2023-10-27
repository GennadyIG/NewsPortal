from .models import Comment, Post, Category
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('post_title', 'post_text')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('comment_text',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
