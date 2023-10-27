# Generated by Django 4.2.5 on 2023-09-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NPbd', '0002_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_text_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_text_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_title_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_title_ru',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
