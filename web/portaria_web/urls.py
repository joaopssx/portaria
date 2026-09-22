"""Rotas principais do projeto."""

from django.urls import include, path

urlpatterns = [
    path("", include("portaria_app.urls")),
]
