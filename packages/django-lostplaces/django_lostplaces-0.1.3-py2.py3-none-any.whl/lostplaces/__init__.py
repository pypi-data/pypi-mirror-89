#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

settings.THUMBNAIL_ALIASES = {
    '': {
        'thumbnail': {'size': (300, 200), 'sharpen': True, 'crop': True},
        'hero': {'size': (700, 466), 'sharpen': True, 'crop': True},
        'large': {'size': (1920, 1920), 'sharpen': True, 'crop': False},
    },
}