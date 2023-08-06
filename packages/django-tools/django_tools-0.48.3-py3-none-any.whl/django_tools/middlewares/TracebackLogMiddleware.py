"""
    Put this into your settings:
    --------------------------------------------------------------------------
        MIDDLEWARE_CLASSES = (
            ...
            'django_tools.middlewares.TracebackLogMiddleware.TracebackLogMiddleware',
            ...
        )
    --------------------------------------------------------------------------

    :copyleft: 2016 by the django-tools team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging


try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object  # fallback for Django < 1.10


class TracebackLogMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        logging.exception(f'Exception on url: {request.path}')
