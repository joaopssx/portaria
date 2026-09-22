"""Configuracao do app da portaria."""

from django.apps import AppConfig


class PortariaAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "portaria_app"
    verbose_name = "Portaria"
