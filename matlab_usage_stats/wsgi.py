"""
WSGI config for matlab_usage_stats project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "matlab_usage_stats.settings")

application = get_wsgi_application()
