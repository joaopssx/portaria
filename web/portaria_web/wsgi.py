"""Ponto de entrada WSGI (usado ao publicar o site em um servidor)."""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR.parent / "src"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portaria_web.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
