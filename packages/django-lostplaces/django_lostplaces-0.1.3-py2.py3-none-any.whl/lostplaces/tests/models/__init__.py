#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import FieldDoesNotExist
from django.test import TestCase


class ModelTestCase(TestCase):
    '''
    Base class for ModelTests.
    Parameters:
    - model : Class to test
    '''
    model = None

    def assertField(self, field_name, field_class, must_have={}, must_not_have={}):
        '''
        Tests if a field exists under the given name and
        if the field is of the right type.
        Also checks if the field has the given must_have attributes
        and does not have any of the must_not_have attributes. If you
        dont care about the value of the attribute you can just set it to 
        something that fullfills value == False (i.e. '' or 0)
        '''
        try:
            field = self.model._meta.get_field(field_name)
        except FieldDoesNotExist:
            self.fail(
                'Expecting %s to have a field named \'%s\'' % (
                    self.model.__name__,
                    field_name
                )
            )
        self.assertEqual(
            type(field), field_class,
            msg='Expecting type of %s to be %s' % (
                str(field),
                field_class.__name__
            )
        )

        for key, value in must_have.items():
            if value:
                self.assertEqual(
                    getattr(field, key), value,
                    msg='Expeting the value of %s %s to be \'%s\'' % (
                        str(field),
                        key,
                        value
                    )
                )
            else:
                self.assertTrue(
                    hasattr(field, key),
                    msg='Expeting %s to have \'%s\'' % (
                        str(field),
                        key
                    )
                )

        for key, value in must_not_have.items():
            if value:
                self.assertTrue(
                    getattr(field, key) != value,
                    msg='Expeting the value of %s %s to not be \'%s\'' % (
                        str(field),
                        key,
                        value
                    )
                )
            else:
                self.assertFalse(
                    hasattr(field, value),
                    msg='Expeting %s to not have \'%s\'' % (
                        str(field),
                        key
                    )
                )

        return field

    def assertCharField(self, field_name, min_length, max_length, must_have={}, must_hot_have={}):
        '''
        Tests if the given field is a char field and if its max_length
        is in min_length and max_legth
        '''
        field = self.assertField(
            field_name, models.CharField, must_have, must_hot_have)
        self.assertTrue(
            field.max_length in range(min_length, max_length),
            msg='Expeting %s  max_length to be in the range of %d and %d' % (
                str(field),
                min_length,
                max_length
            )
        )

    def assertFloatField(self, field_name, min_value=None, max_value=None, must_have={}, must_hot_have={}):
        '''
        Tests if the field is a floatfield. If min_value and/or max_value are passed,
        the validators of the field are also checked. The validator list of the field should
        look like 
        [MinValueValidator, MayValueValidator], if both values are passed,
        [MinValueValidator] if only min_value is passed,
        [MaxValueValidator] if only max_value is passed
        '''
        field = self.assertField(
            field_name, models.FloatField, must_have, must_hot_have)
        if min_value:
            self.assertTrue(
                len(field.validators) >= 1,
                msg='Expecting the first valiator of %s to check the minimum' % (
                    str(field)
                )
            )
            self.assertEqual(
                field.validators[0].limit_value,
                min_value,
                msg='Expecting the min value of %s min to be at least %d' % (
                    str(field),
                    min_value
                )
            )
        if max_value:
            index = 0
            if min_value:
                index += 1
            self.assertTrue(
                len(field.validators) >= index+1,
                msg='Expecting the second valiator of %s to check the maximum' % (
                    str(field)
                )
            )
            self.assertEqual(
                field.validators[1].limit_value,
                max_value,
                msg='Expecting the max value of %s min to be at most %d' % (
                    str(field),
                    max_value
                )
            )
