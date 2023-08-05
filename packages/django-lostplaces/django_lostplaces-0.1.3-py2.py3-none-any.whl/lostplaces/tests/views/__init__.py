#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from lostplaces.models import Taggable, Mapable

from taggit.models import Tag

class ViewTestCase(TestCase):
    '''
    This is a Mixin for testing views. It provides functionality to
    test the context, forms and HTTP Response of responses. 
    All methods take responses, so this base class can be used
    with django's RequestFactory and Test-Client
    '''
    view = None
    
    def assertContext(self, response, key, value=None):
        '''
        Checks weather the response's context has the given key
        and, if passed, checks the value
        '''
        self.assertTrue(
            key in response.context,
            msg='Expecting the context of %s to have an attribute \'%s\'' % (
                self.view.__name__,
                key
            )
        )

        if value:
            self.assertEqual(
                value,
                response.context[key],
                msg='Expecting the context of %s to have %s set to \'%s\'' % (
                    self.view.__name__,
                    key, 
                    str(value)
                )
            )
        
    def assertHasForm(self, response, key, form_class):
        '''
        Checks if response has a form under the given key and if 
        the forms class matches.
        '''
        self.assertContext(response, key)
        self.assertEqual(
            type(response.context[key]),
            form_class,
            msg='Expecting %s\'s context.%s to be of the type %s' % (
                self.view.__name__,
                key,
                form_class.__name__
            ) 
        )

    def assertHttpCode(self, response, code):
        '''
        Checks if the response has the given status code
        '''
        self.assertEqual(
            response.status_code, code,
            msg='Expecting an HTTP %s response, but got HTTP %s' % (
                code,
                response.status_code
            )
        )
        
    def assertHttpRedirect(self, response, redirect_to=None):
        '''
        Checks weather the response redirected, and if passed, 
        if it redirected to the expected location
        '''
        
        self.assertTrue(
            300 <= response.status_code < 400,
            'Expected an HTTP 3XX (redirect) response, but got HTTP %s' %
            response.status_code
        )
        self.assertTrue(
            'location' in response,
            msg='Expecting a redirect to have an location, got none'
        )
        if redirect_to:
            self.assertEqual(
                response['location'],
                redirect_to,
                msg='Expecting the response to redirect to %s, where redirected to %s instea' % (
                    str(redirect_to),
                    str(response['location'])
                )
            )

    def assertHttpOK(self, response):
        self.assertHttpCode(response, 200)

    def assertHttpCreated(self, response):
        self.assertHttpCode(response, 201)

    def assertHttpBadRequest(self, response):
        self.assertHttpCode(response, 400)

    def assertHttpUnauthorized(self, response):
        self.assertHttpCode(response, 401)

    def assertHttpForbidden(self, response):
        self.assertHttpCode(response, 403)

    def assertHttpNotFound(self, response):
        self.assertHttpCode(response, 404)

    def assertHttpMethodNotAllowed(self, response):
        self.assertHttpCode(response, 405)
        
class TaggableViewTestCaseMixin:

    def assertTaggableContext(self, context):
        self.assertTrue(
            'all_tags' in context,
            msg='Expecting the context for taggable to contain an \'all_tags\' attribute'
        )
        
        for tag in context['all_tags']:
            self.assertTrue(
                isinstance(tag, Tag),
                msg='Expecting all entries to be an instance of %s, got %s' % (
                    str(Tag),
                    str(type(tag))
                )
            )
            
        self.assertTrue(
            'submit_form' in context,
            msg='Expecting the context for taggable to contain \'submit_form\' attribute'
        )
        
        self.assertTrue(
            'tagged_item' in context,
            msg='Expecting the context for taggable to contain \'tagged_item\' attribute'
        )
        
        self.assertTrue(
            isinstance(context['tagged_item'], Taggable),
            msg='Expecting the tagged_item to be an instance of %s' % (
                str(Taggable)
            )
        )
        
        self.assertTrue(
            'submit_url_name' in context,
            msg='Expecting the context for taggable to contain \'submit_url_name\' attribute'
        )
        
        self.assertTrue(
            type(context['submit_url_name']) == str,
            msg='Expecting submit_url_name to be of type string'
        )
        
        self.assertTrue(
            'delete_url_name' in context,
            msg='Expecting the context for taggable to contain \'delete_url_name\' attribute'
        )
        
        self.assertTrue(
            type(context['delete_url_name']) == str,
            msg='Expecting delete_url_name to be of type string'
        )
        
class MapableViewTestCaseMixin:
    
    def assertMapableContext(self, context):
        self.assertTrue(
            'all_points' in context,
            msg='Expecting the context for mapable point to contain \'all_points\' attribute'
        )
        
        for point in context['all_points']:
            self.assertTrue(
                isinstance(point, Mapable),
                msg='Expecting all entries to be an instance of %s, got %s' % (
                    str(Mapable),
                    str(type(point))
                )
            )
            
        self.assertTrue(
            'map_center' in context,
            msg='Expecting the context for mapable point to contain \'map_center\' attribute'
        )
        
        self.assertTrue(
            'latitude' in context['map_center'],
            msg='Expecting the map center to contain an \'latitude\' attribute'
        )
        
        self.assertTrue(
            isinstance(context['map_center']['latitude'], float) or isinstance(context['map_center']['latitude'], int),
            msg='Expecting the latitude of the map center to be numeric, type %s given' % (
                str(type(context['map_center']['latitude']))
            )
        )
        
        self.assertTrue(
            -90 <= context['map_center']['latitude'] <= 90,
            msg='Expecting the latitude of map center to be in the range of -90 and 90'
        )
        
        self.assertTrue(
            'longitude' in context['map_center'],
            msg='Expecting the map center to contain an \'longitude\' attribute'
        )
        
        self.assertTrue(
            isinstance(context['map_center']['longitude'], float) or isinstance(context['map_center']['longitude'], int),
            msg='Expecting the longitude of the map center to be numeric, type %s given' % (
                str(type(context['map_center']['longitude']))
            )
        )
        
        self.assertTrue(
            -180 <= context['map_center']['longitude'] <= 180,
            msg='Expecting the longitude of map center to be in the range of -180 and 180'
        )
            
        