#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.utils import timezone
from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User

from lostplaces.models import (
    Taggable,
    Mapable,
    Submittable,
    PlaceAsset,
    Expireable,
    Voucher
)
from lostplaces.tests.models import ModelTestCase

from taggit.managers import TaggableManager


class TaggableTestCase(ModelTestCase):

    model = Taggable

    def test_tags(self):
        self.assertField('tags', TaggableManager)


class MapableTestCase(ModelTestCase):

    model = Mapable

    def test_name(self):
        self.assertCharField(
            field_name='name',
            min_length=10,
            max_length=100
        )

    def test_latitude(self):
        self.assertFloatField(
            field_name='latitude',
            min_value=-90,
            max_value=90
        )

    def test_longitude(self):
        self.assertFloatField(
            field_name='longitude',
            min_value=-180,
            max_value=180
        )
        
class SubmittableTestCase(ModelTestCase):
    model = Submittable

    def test_submitted_when(self):
        self.assertField(
            field_name='submitted_when',
            field_class=models.DateTimeField,
            must_have={'auto_now_add': True}
        )

    def test_submitted_by(self):
        submitted_by = self.assertField(
            field_name='submitted_by',
            field_class=models.ForeignKey
        )
        self.assertEqual(
            submitted_by.remote_field.related_name,
            '%(class)ss',
            msg='Expecting the related_name of %s to be \'%%(class)ss\', got %s' % (
                str(submitted_by),
                submitted_by.remote_field.related_name
            )
        )
        self.assertTrue(
            submitted_by.null,
            msg='Expecting %s to has null=True' % (
                str(submitted_by)
            )
        )
        self.assertTrue(
            submitted_by.blank,
            msg='Expecting %s to has blank=True' % (
                str(submitted_by)
            )    
        )
        self.assertEqual(
            submitted_by.remote_field.on_delete,
            models.SET_NULL,
            msg='Expecting %s to be null when reference is delete (models.SET_NULL)' % (
                str(submitted_by)
            )
        )

class PlaceAssetTestCase(ModelTestCase):
    model = PlaceAsset

    def test_place(self):
        field = self.assertField('place', models.ForeignKey)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE,
            msg='Expecting the deletion of %s to be cascading' % (
                str(field)
            )
        )
        expected_related_name = '%(class)ss'
        self.assertEqual(field.remote_field.related_name, expected_related_name,
            msg='Expecting the related name of %s to be %s' % (
                str(field),
                expected_related_name
            )
        )

class ExpireableTestCase(ModelTestCase):
    model = Expireable
    
    def test_fields(self):
        self.assertField(
            field_name='created_when',
            field_class=models.DateTimeField,
            must_have={'auto_now_add': True}
        )
        self.assertField(
            field_name='expires_when',
            field_class=models.DateTimeField
        )
        
    def test_is_expired(self):
        valid_voucher = Voucher.objects.create(
            code='Test123',
            expires_when=timezone.now() + datetime.timedelta(minutes=2)
        )
        self.assertFalse(
            valid_voucher.is_expired,
            msg='Expecing the expirable object to not be expired'
        )
        
        invalid_voucher = Voucher.objects.create(
            code='Test1234',
            expires_when=timezone.now() - datetime.timedelta(minutes=2)
        )
        self.assertTrue(
            invalid_voucher.is_expired,
            msg='Expecing the expirable object to be expired'
        )