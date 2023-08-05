#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from lostplaces.models import Place

class IsAuthenticatedMixin(LoginRequiredMixin, View):
    '''
    A view mixin that checks wether a user is logged in or not.
    If the user is not logged in, he gets redirected to 
    the login page.
    '''
    login_url = reverse_lazy('login')
    permission_denied_message = _('Please login to proceed')

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()

class IsPlaceSubmitterMixin(UserPassesTestMixin, View):
    '''
    A view mixin that checks wether a user is the submitter
    of a place, throws 403 if the user is not. The subclass 
    has to provide a get_place method, which returns the
    place to check.
    '''
    place_submitter_error_message = None

    def get_place(self):
        pass

    def test_func(self):
        """ Check if user is eligible to modify place. """

        if not hasattr(self.request, 'user'):
            return False

        if self.request.user.is_superuser:
            return True
        
        # Check if currently logged in user was the submitter
        place_obj = self.get_place()

        if place_obj and hasattr(place_obj, 'submitted_by') and self.request.user.explorer == place_obj.submitted_by:
            return True

        if self.place_submitter_error_message:
            messages.error(self.request, self.place_submitter_error_message)
        return False

class PlaceAssetCreateView(IsAuthenticatedMixin, SuccessMessageMixin, CreateView):
    model = None
    template_name = ''
    success_message = ''

    def get(self, request, place_id, *args, **kwargs):
        self.place = get_object_or_404(Place, pk=place_id)
        return super().get(request, *args, **kwargs)

    def post(self, request, place_id, *args, **kwargs):
        self.place = get_object_or_404(Place, pk=place_id)
        response = super().post(request, *args, **kwargs)
        self.object.place = self.place
        self.object.submitted_by = request.user.explorer
        self.object.save()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place'] = self.place
        return context

    def get_success_url(self):
        return reverse_lazy('place_detail', kwargs={'pk': self.place.id})

class PlaceAssetDeleteView(IsAuthenticatedMixin, IsPlaceSubmitterMixin, SingleObjectMixin, View):
    model = None
    success_message = ''
    permission_denied_message = ''

    def get_place(self):
        place_id = self.get_object().place.id
        return Place.objects.get(pk=place_id)

    def test_func(self):
        can_edit_place = super().test_func()
        if can_edit_place:
            return True
        
        if self.get_object().submitted_by == self.request.user.explorer:
            return True
        
        messages.error(self.request, self.permission_denied_message)
        return False

    def get(self, request, *args, **kwargs):
        place_id = self.get_object().place.id
        self.get_object().delete()
        messages.success(self.request, self.success_message)
        return redirect(reverse_lazy('place_detail', kwargs={'pk': place_id}))
