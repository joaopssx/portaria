"""Configuracao do projeto Django da portaria.

Mantida no minimo necessario para uma pagina web simples: sem banco de
dados proprio do Django, porque os dados continuam vindo dos arquivos CSV
gravados pela camada de persistencia em src/persistence/.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Reaproveita as classes de dominio que ja existem em src/.
sys.path.insert(0, str(BASE_DIR.parent / "src"))

# Em um sistema de verdade esta chave viria de uma variavel de ambiente.
SECRET_KEY = "chave-de-desenvolvimento-nao-usar-em-producao"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "portaria_app",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "portaria_web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "portaria_web.wsgi.application"

# Nao usamos o ORM do Django: a persistencia e em CSV.
DATABASES = {}

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
