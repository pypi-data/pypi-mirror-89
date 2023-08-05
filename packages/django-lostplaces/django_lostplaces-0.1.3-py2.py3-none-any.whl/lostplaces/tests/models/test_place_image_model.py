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

from lostplaces.models import PlaceImage, Place
from lostplaces.tests.models import ModelTestCase

from easy_thumbnails.fields import ThumbnailerImageField

class PlaceImageTestCase(ModelTestCase):
    model = PlaceImage

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
        place.tags.add('I a tag', 'testlocation')
        place.save()

        if not os.path.isdir(settings.MEDIA_ROOT):
            os.mkdir(settings.MEDIA_ROOT)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'im_a_image_copy.jpeg')):
            shutil.copyfile(
                os.path.join(current_dir, 'im_a_image.jpeg'),
                os.path.join(settings.MEDIA_ROOT, 'im_a_image_copy.jpeg')
            )
            
            shutil.copyfile(
                os.path.join(current_dir, 'im_a_image.jpeg'),
                os.path.join(settings.MEDIA_ROOT, 'im_a_image_changed.jpeg')
            )
            
        PlaceImage.objects.create(
            description='Im a description',
            filename=os.path.join(settings.MEDIA_ROOT, 'im_a_image_copy.jpeg'),
            place=place,
            submitted_when=timezone.now(),
            submitted_by=user.explorer
        )

    def setUp(self):
        self.place_image = PlaceImage.objects.get(id=1)

    def test_description(self):
        self.assertField('description', models.TextField)

    def test_filename(self):
        self.assertField('filename',ThumbnailerImageField)

    def test_place(self):
        field = self.assertField('place', models.ForeignKey)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE,
            msg='Expecting the deletion of %s to be cascading' % (
                str(field)
            )
        )
        expected_related_name = 'placeimages'
        self.assertEqual(field.remote_field.related_name, expected_related_name,
            msg='Expecting the related name of %s to be %s' % (
                str(field),
                expected_related_name
            )
        )

    def test_change_filename(self):
        path = self.place_image.filename.path
        self.place_image.filename = os.path.join(settings.MEDIA_ROOT, 'im_a_image_changed.jpeg')
        self.place_image.save()
        self.assertFalse(
            os.path.isfile(path),
            msg='Expecting the old file of an place_image to be deleteed when an place_image file is changed'
        )
        
    def test_deletion(self):
        path = self.place_image.filename.path
        self.place_image.delete()
        self.assertFalse(
            os.path.isfile(path),
            msg='Expecting the file of an place_image to be deleteed when an place_image is deleted'
        )