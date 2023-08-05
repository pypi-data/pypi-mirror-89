# -*- python -*-
"""
djfim.apps
"""

from django.apps import AppConfig


class DjFIMConfig(AppConfig):
    name = 'djfim'
    verbose_name = "Django FIM"

    def ready(self):
        pass  # NOQA
