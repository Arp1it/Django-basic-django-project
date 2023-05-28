from django.apps import AppConfig


class ChjConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chj'

    # def ready(self):
    #     from . import signals
