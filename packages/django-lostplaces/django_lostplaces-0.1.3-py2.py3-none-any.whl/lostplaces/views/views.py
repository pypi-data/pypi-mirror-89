#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import View
from django.views.generic.edit import CreateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _

from lostplaces.forms import ExplorerCreationForm, TagSubmitForm
from lostplaces.models import Place, PhotoAlbum
from lostplaces.views.base_views import IsAuthenticatedMixin

from lostplaces.views.base_views import (
    PlaceAssetCreateView, 
    PlaceAssetDeleteView,
)

from taggit.models import Tag

class SignUpView(SuccessMessageMixin, CreateView):
    form_class = ExplorerCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    success_message = _('User created')

class HomeView(IsAuthenticatedMixin, View):
    def get(self, request, *args, **kwargs):
        place_list = Place.objects.all().order_by('-submitted_when')[:10]
        context = {
            'place_list': place_list,
            'mapping_config': {
                'all_points': place_list,
                'map_center': Place.average_latlon(place_list)
            }
        }
        return render(request, 'home.html', context)

    def handle_no_permission(self):
        place_list = Place.objects.all().order_by('-submitted_when')[:5]
        context = {
            'place_list': place_list
        }
        return render(self.request, 'home_unauth.html', context)

class PhotoAlbumCreateView(PlaceAssetCreateView):
    model = PhotoAlbum
    fields = ['url', 'label']
    template_name = 'photo_album/photo_album_create.html'
    success_message = _('Photo album link submitted')

class PhotoAlbumDeleteView(PlaceAssetDeleteView):
    model = PhotoAlbum
    pk_url_kwarg = 'pk'
    success_message = _('Photo album link deleted')
    permission_denied_messsage = _('You are not allowed to edit this photo album link')

class PlaceTagSubmitView(IsAuthenticatedMixin, View):
	def post(self, request, tagged_id, *args, **kwargs):
		place = get_object_or_404(Place, pk=tagged_id)
		form = TagSubmitForm(request.POST)
		if form.is_valid():
			tag_list_raw = form.cleaned_data['tag_list']
			tag_list_raw = tag_list_raw.strip().split(',')
			tag_list = []
			for tag in tag_list_raw:
				tag_list.append(tag.strip())
			place.tags.add(*tag_list)
			place.save()

		return redirect(reverse_lazy('place_detail', kwargs={'pk': place.id}))

class PlaceTagDeleteView(IsAuthenticatedMixin, View):
    def get(self, request, tagged_id, tag_id, *args, **kwargs):
        place = get_object_or_404(Place, pk=tagged_id)
        tag = get_object_or_404(Tag, pk=tag_id)
        place.tags.remove(tag)
        return redirect(reverse_lazy('place_detail', kwargs={'pk': tagged_id}))

def FlatView(request, slug):
    if request.LANGUAGE_CODE == 'de':
        return render(request, 'flat/' + slug + '-de' + '.html')
    else:
        return render(request, 'flat/' + slug + '.html')
