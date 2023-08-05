#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

from lostplaces.models import Place
from lostplaces.tests.models import ModelTestCase

class PlaceTestCase(ModelTestCase):
    model = Place
    related_name = 'places'
    nullable = True

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
        self.place = Place.objects.get(id=1)

    def test_location(self):
        self.assertCharField(
            field_name='location',
            min_length=10,
            max_length=100
        )

    def test_description(self):
        self.assertField('description', models.TextField)

    def test_average_latlon(self):
        '''
        Tests the average latitude/longitude calculation of a list
        of 10 places
        '''
        place_list = []
        for i in range(10):
            place = Place.objects.get(id=1)
            place.id = None
            place.latitude = i+1
            place.longitude = i+10
            place.save()
            place_list.append(place)

        avg_latlon = Place.average_latlon(place_list)
        
        self.assertTrue('latitude' in avg_latlon,
            msg='Expecting avg_latlon dict to have an \'latitude\' key'
        )
        self.assertTrue('longitude' in avg_latlon,
            msg='Expecting avg_latlon dict to have an \'longitude\' key'
        )
        
        self.assertEqual(avg_latlon['latitude'], 5.5,
            msg='%s: average latitude missmatch' % (
                self.model.__name__
            )
        )
        self.assertEqual(avg_latlon['longitude'], 14.5,
            msg='%s: average longitude missmatch' % (
                self.model.__name__
            )
        )

    def test_average_latlon_one_place(self):
        '''
        Tests the average latitude/longitude calculation of a list
        of one place
        '''
        place = Place.objects.get(id=1)
        avg_latlon = Place.average_latlon([place])
        self.assertEqual(avg_latlon['latitude'], place.latitude,
            msg='%s:(one place) average latitude missmatch' % (
                self.model.__name__
            )
        )
        self.assertEqual(avg_latlon['longitude'], place.longitude,
            msg='%s: (one place) average longitude missmatch' % (
                self.model.__name__
            )
        )

    def test_average_latlon_no_places(self):
        '''
        Tests the average latitude/longitude calculation of 
        an empty list
        '''
        avg_latlon = Place.average_latlon([])
        self.assertEqual(avg_latlon['latitude'], 0,
            msg='%s: (no places) average latitude missmatch' % (
                self.model.__name__
            )
        )
        self.assertEqual(avg_latlon['longitude'], 0,
            msg='%s: (no places) average longitude missmatch' % (
                self.model.__name__
            )
        )

    def test_str(self):
        place = self.place
        self.assertTrue(place.name.lower() in str(place).lower(),
            msg='Expecting %s.__str__ to contain the name' % (
                self.model.__name__
            )
        )
