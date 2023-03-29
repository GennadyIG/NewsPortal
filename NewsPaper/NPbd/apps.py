from django.apps import AppConfig


class NpbdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NPbd'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
