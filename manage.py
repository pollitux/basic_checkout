#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

Run this file from INSIDE the basic_checkout/ directory:
    cd basic_checkout
    python manage.py runserver
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Could not import Django.") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
