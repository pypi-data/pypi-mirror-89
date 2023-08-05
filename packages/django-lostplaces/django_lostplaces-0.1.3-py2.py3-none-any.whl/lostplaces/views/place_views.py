#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models.functions import Lower

from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from lostplaces.models import Place, PlaceImage
from lostplaces.views.base_views import IsAuthenticatedMixin, IsPlaceSubmitterMixin
from lostplaces.views.place_image_views import MultiplePlaceImageUploadMixin
from lostplaces.forms import PlaceForm, PlaceImageForm, TagSubmitForm

from taggit.models import Tag

class PlaceListView(IsAuthenticatedMixin, ListView):
    paginate_by = 5
    model = Place
    template_name = 'place/place_list.html'
    ordering = [Lower('name')]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapping_config'] = {
            'all_points': context['place_list'],
            'map_center': Place.average_latlon(context['place_list'])
        }
        return context

class PlaceDetailView(IsAuthenticatedMixin, View):
    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        context = {
            'place': place,
            'mapping_config': {
                'all_points': [ place ],
                'map_center': {'latitude': place.latitude, 'longitude': place.longitude},                                
            },
            'tagging_config': {
                'all_tags': Tag.objects.all(),
                'submit_form': TagSubmitForm(),
                'tagged_item': place,
                'submit_url_name': 'place_tag_submit',
                'delete_url_name': 'place_tag_delete'
            }
        }
        return render(request, 'place/place_detail.html', context)

class PlaceUpdateView(IsAuthenticatedMixin, IsPlaceSubmitterMixin, SuccessMessageMixin, UpdateView):
    template_name = 'place/place_update.html'
    model = Place
    form_class = PlaceForm
    success_message = _('Successfully updated place')
    place_submitter_error_message = _('You are not allowed to edit this place')

    def get_success_url(self):
        return reverse_lazy('place_detail', kwargs={'pk':self.get_object().pk})

    def get_place(self):
        return self.get_object()

class PlaceCreateView(MultiplePlaceImageUploadMixin, IsAuthenticatedMixin, View):

    def get(self, request, *args, **kwargs):
        place_image_form = PlaceImageForm()
        place_form = PlaceForm()

        context = {
            'place_form': place_form,
            'place_image_form': place_image_form
        }
        return render(request, 'place/place_create.html', context)

    def post(self, request, *args, **kwargs):
        place_form = PlaceForm(request.POST)

        if place_form.is_valid():
            submitter = request.user.explorer
            place = place_form.save(commit=False)
            # Save logged in user as "submitted_by"
            place.submitted_by = submitter
            place.save()

            self.handle_place_images(request, place)
            
            messages.success(
                self.request,
                _('Successfully created place')
            )
            return redirect(reverse_lazy('place_detail', kwargs={'pk': place.pk}))
        
        else:
            # Usually the browser should have checked the form before sending.
            messages.error(
                self.request,
                _('Please fill in all required fields.')
            )
            return render(request, 'place/place_create.html', context={'form': place_form})

class PlaceDeleteView(IsAuthenticatedMixin, IsPlaceSubmitterMixin, DeleteView):
    template_name = 'place/place_delete.html'
    model = Place
    success_message = _('Successfully deleted place')
    success_url = reverse_lazy('place_list')
    place_submitter_error_message = _('You are not allowed to delete this place')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_place(self):
        return self.get_object()
