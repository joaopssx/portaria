"""Rotas do app da portaria."""

from django.urls import path

from portaria_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pessoas/", views.pessoas, name="pessoas"),
    path("cadastrar/", views.cadastrar, name="cadastrar"),
    path("acesso/", views.acesso, name="acesso"),
]
