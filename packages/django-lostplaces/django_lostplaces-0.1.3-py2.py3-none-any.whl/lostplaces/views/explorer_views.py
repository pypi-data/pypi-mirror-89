#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import View

from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from lostplaces.common import get_all_subclasses
from lostplaces.views.base_views import IsAuthenticatedMixin
from lostplaces.models.models import Explorer
from lostplaces.models.place import Place, PlaceAsset

class ExplorerProfileView(IsAuthenticatedMixin, View):
    def get(self, request, explorer_id):
        explorer = get_object_or_404(Explorer, pk=explorer_id)
        place_list = Place.objects.filter(submitted_by=explorer)
        place_count = place_list.count()

        context={
            'explorer': explorer,
            'place_count': place_count,
            'place_list': place_list,
            'assets': {}
        }

        asset_count = 0
        for subclass in get_all_subclasses(PlaceAsset): # kinda ugly, but PlaceAsset cannot be abstract according to django ORM
            objects = subclass.objects.filter(submitted_by=explorer)
            context['assets'][subclass.__name__.lower()+'s'] = objects
            asset_count += objects.count()
        
        context['asset_count'] = asset_count
        
        print(context['assets'])
        
        return render(
            request=request,
            template_name='explorer/profile.html',
            context=context
        )
        
        