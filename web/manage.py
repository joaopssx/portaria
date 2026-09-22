#!/usr/bin/env python
"""Utilitario de linha de comando do Django."""

import os
import sys
from pathlib import Path


def main():
    # Coloca a pasta src/ no caminho de importacao para reaproveitar as
    # classes de dominio ja escritas (models, services, persistence).
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE_DIR.parent / "src"))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portaria_web.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django nao esta instalado. Rode: pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
