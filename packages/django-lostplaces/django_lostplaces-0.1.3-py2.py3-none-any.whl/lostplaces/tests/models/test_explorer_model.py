#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User

from lostplaces.models import Explorer

class ExplorerTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        User.objects.create_user(
            username='testpeter',
            password='Develop123'
        )

    def test_epxlorer_creation(self):
        '''
        Tests if the explorer profile will be automticly
        created when a user is created
        '''
        
        user = User.objects.get(id=1)
        explorer_list = Explorer.objects.all()
        self.assertTrue(len(explorer_list) > 0,
            msg='Expecting at least one Exlorer object, none found'
        )
        self.assertTrue(hasattr(user, 'explorer'),
            msg='''Expecting the User instance to have an \'explorer\' attribute. 
            Check the Explorer model and the related name.'''
        )
        
        explorer = Explorer.objects.get(id=1)
        self.assertEqual(explorer, user.explorer,
            msg='''The Explorer object of the User did not match.
            Expecting User with id 1 to have Explorer with id 1'''
        )
        
        explorer = Explorer.objects.get(id=1)
        self.assertEqual(explorer.user, user,
            msg='''The User object of the Explorer did not match.
            Expecting Explorer with id 1 to have User with id 1'''
        )
        
    def test_explorer_deletion(self):
        '''
        Tests if the Explorer objects get's deleted when the User instance is deleted
        '''
        
        user = User.objects.get(username='testpeter')
        explorer_id = user.explorer.id
        user.delete()
        with self.assertRaises(models.ObjectDoesNotExist,
            msg='Expecting explorer objec to be deleted when the corresponding User object is deleted'
            ):
            Explorer.objects.get(id=explorer_id)
        
        
    