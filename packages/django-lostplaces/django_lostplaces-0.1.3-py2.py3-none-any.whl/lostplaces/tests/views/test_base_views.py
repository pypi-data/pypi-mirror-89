#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory, Client
from django.urls import reverse_lazy
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.utils import timezone

from lostplaces.models import Place
from lostplaces.views import IsAuthenticatedMixin
from lostplaces.tests.views import ViewTestCase

class TestIsAuthenticated(ViewTestCase):
    view = IsAuthenticatedMixin

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testpeter',
            password='Develop123'
        )
        
    def setUp(self):
        self.client = Client()

    def test_logged_in(self):
        request = RequestFactory().get('/')
        request.user = User.objects.get(id=1)

        response = IsAuthenticatedMixin.as_view()(request)
        # Expecting a 405 because IsAuthenticatedMixin has no 'get' method
        self.assertHttpMethodNotAllowed(response)

    def test_not_logged_in(self):
        request = RequestFactory().get('/someurl1234')
        request.user = AnonymousUser()
        request.session = 'session'
        messages = FallbackStorage(request)
        request._messages = messages

        response = IsAuthenticatedMixin.as_view()(request)
        self.assertHttpRedirect(response, '?'.join([str(reverse_lazy('login')), 'next=/someurl1234']))
        
        response = self.client.get(response['Location']) 
        self.assertTrue(len(messages) > 0)

class TestIsPlaceSubmitterMixin(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testpeter',
            password='Develop123'
        )
        
        place = Place.objects.create(
            name='Im a place',
            submitted_when=timezone.now(),
            submitted_by=user.explorer,
            location='Testtown',
            latitude=50.5,
            longitude=7.0,
            description='This is just a test, do not worry'
        )
        place.tags.add('I a tag', 'testlocation')
        place.save()
        
    def setUp(self):
        self.client = Client()

    def setUp(self):
        self. client = Client()

    def test_is_submitter(self):
        self.client.login(username='testpeter', password='Develop123')
        response = self.client.get(reverse_lazy('place_edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_is_no_submitter(self):
        User.objects.create_user(
            username='manfred',
            password='Develop123'
        )
        self.client.login(username='manfred', password='Develop123')
        response = self.client.get(reverse_lazy('place_edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.context['messages'])
        self.assertTrue(len(response.context['messages']) > 0)