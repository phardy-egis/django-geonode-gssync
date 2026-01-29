from django.apps import AppConfig
import os

class GssyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gssync'
    path = os.path.dirname(os.path.abspath(__file__))
