from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


class PostcategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostcategoryInline,)


class PostAdmin(admin.ModelAdmin):
    inlines = (PostcategoryInline,)
    list_display = ['post_title', 'author', 'get_category']
    list_filter = ['author', 'category']
    search_fields = ['post_title', 'category__name']

    def get_category(self, obj):
        return ', '.join([cat.name for cat in obj.category.all()])


admin.site.register(Post, PostAdmin)
# admin.site.register(Author)
# admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
# Register your models here.
