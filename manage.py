#!/usr/bin/env python
"""
Punto de entrada del proyecto Django.

Uso habitual:
  python manage.py runserver     → arranca el servidor web local
  python manage.py migrate       → aplica cambios de modelos a la base de datos
  python manage.py createsuperuser → crea usuario para /admin/
"""
import os
import sys


def main():
    """
    Configura Django y ejecuta el comando que escribas en la terminal.

    Ejemplo: python manage.py runserver
    → Django carga instagram.settings y ejecuta el servidor en el puerto 8000.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
