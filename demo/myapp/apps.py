from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    def ready(self):
        import myapp.signals