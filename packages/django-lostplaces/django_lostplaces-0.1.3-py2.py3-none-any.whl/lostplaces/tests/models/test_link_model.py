#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from unittest import mock

from django.test import TestCase
from django.db import models
from django.core.files import File
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from lostplaces.models import ExternalLink, PhotoAlbum, Place
from lostplaces.tests.models import ModelTestCase


class ExternalLinkTestCase(ModelTestCase):
    model = ExternalLink

    def setup(self):
        self.albumlink = ExternalLink.objects.get(id=1)

    def test_label(self):
        self.assertField('label', models.CharField)

    def test_url(self):
        self.assertField('url', models.URLField)
    
class PhotoAlbumTestCase(ModelTestCase):
    model = PhotoAlbum
    
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testpeter',
            password='Develop123'
        )
    
        place = Place.objects.create(
            name='Im a place',
            submitted_when=timezone.now(),
            submitted_by=User.objects.get(username='testpeter').explorer,
            location='Testtown',
            latitude=50.5,
            longitude=7.0,
            description='This is just a test, do not worry'
        )
        place.tags.add('I am a tag', 'testlocation')
        place.save()

        PhotoAlbum.objects.create(
            url='https://lostplaces.example.com/album/',
            label='TestLink',
            submitted_by=user.explorer,
            place=place,
            submitted_when=timezone.now()
        )
        
    def setUp(self):
        self.albumlink = PhotoAlbum.objects.get(id=1)
        self.place = Place.objects.get(id=1)

    def test_place(self):
        field = self.assertField('place', models.ForeignKey)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE,
            msg='Expecting the deletion of %s to be cascading' % (
                str(field)
            )
        )
        expected_related_name = 'photoalbums'
        self.assertEqual(field.remote_field.related_name, expected_related_name,
            msg='Expecting the related name of %s to be %s' % (
                str(field),
                expected_related_name
            )
        )

    def test_label(self):
        albumlink = self.albumlink
    
        self.assertTrue('TestLink' in albumlink.label,
            msg='Expecting albumlink.label to contain \'TestLink\' string'
        )

    def test_url(self):
        albumlink = self.albumlink
    
        self.assertTrue('lostplaces.example.com' in albumlink.url,
            msg='Expecting albumlink.url to contain \'lostplaces.example.com\' string'
        )
        
    def test_linked_place(self):
        albumlink = self.albumlink
        place = self.place
        self.assertTrue(str(albumlink.place) in str(place.name),
            msg='Expecting %s.__str__ to contain the name' % (
                self.model.__name__
            )
        )
