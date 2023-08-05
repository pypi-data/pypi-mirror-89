#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


from lostplaces.models import Place
from lostplaces.views import (
    PlaceCreateView,
    PlaceListView,
    PlaceDetailView
)
from lostplaces.forms import PlaceImageForm, PlaceForm
from lostplaces.tests.views import (
    ViewTestCase,
    TaggableViewTestCaseMixin,
    MapableViewTestCaseMixin
)


class TestPlaceCreateView(ViewTestCase):
    view = PlaceCreateView

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

    def test_has_forms(self):
        self.client.login(username='testpeter', password='Develop123')
        response = self.client.get(reverse('place_create'))

        self.assertHasForm(response, 'place_image_form', PlaceImageForm)
        self.assertHasForm(response, 'place_form', PlaceForm)


class TestPlaceListView(ViewTestCase):
    view = PlaceListView

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

    def test_list_view(self):
        self.client.login(username='testpeter', password='Develop123')
        response = self.client.get(reverse('place_list'))

        self.assertContext(response, 'mapping_config')


class PlaceDetailViewTestCase(TaggableViewTestCaseMixin, MapableViewTestCaseMixin, ViewTestCase):
    view = PlaceDetailView

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

    def test_context(self):
        self.client.login(username='testpeter', password='Develop123')
        response = self.client.get(reverse('place_detail', kwargs={'pk': 1}))

        self.assertTrue(
            'tagging_config' in response.context,
            msg='Expecting the context of %s to have an \'tagging_config\'' % (
                str(self.view)
            )
        )
        self.assertTaggableContext(response.context['tagging_config'])

        self.assertTrue(
            'mapping_config' in response.context,
            msg='Expecting the context of %s to have an \'mapping_config\'' % (
                str(self.view)
            )
        )
        self.assertMapableContext(response.context['mapping_config'])
