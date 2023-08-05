#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os
from importlib import import_module

from django.core.cache import cache
from django.conf import settings
from django.template import Library, TemplateSyntaxError

#icons_json_path = getattr(settings, 'SVG_ICONS_SOURCE_FILE')
icons_json_path = os.path.join(settings.BASE_DIR, 'lostplaces', 'static', 'icons', 'icons.icomoon.json')
icons_json = json.load(open(icons_json_path))

register = Library()

@register.inclusion_tag('svg_icon/icon.html')
def icon(name, **kwargs):

	icon_config = icons_json.get(name, None)

	if icon_config:

		width = kwargs.get('width', icon_config.get('width', 16))
		height = kwargs.get('height', icon_config.get('heigh', 16))
		viewBox = kwargs.get('viewBox', icon_config.get('viewBox', '0 0 1024 1024'))

		return {
			'width': kwargs.get('size', width),
			'height': kwargs.get('size', height),
			'className': kwargs.get('className'),
			'viewBox': viewBox,
			'paths': icon_config.get('paths', [''])
		}
