#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.test import TestCase
from django.db import models
from django.utils import timezone

from lostplaces.models import Voucher
from lostplaces.tests.models import ModelTestCase


class VoucherTestCase(ModelTestCase):
    model = Voucher

    @classmethod
    def setUpTestData(cls):
        Voucher.objects.create(
            code='ayDraJCCwfhcFiYmSR5GrcjcchDfcahv',
            expires_when=timezone.now() + datetime.timedelta(days=1)
        )
        
    def setUp(self):
        self.voucher = Voucher.objects.get(id=1)
    
    def test_voucher_code(self):
        self.assertCharField(
            field_name='code',
            min_length=10,
            max_length=100,
            must_have={'unique': True}
        )
        
    def test_voucher_created(self):
        self.assertField(
            field_name='created_when',
            field_class=models.DateTimeField,
            must_have={'auto_now_add': True}
        )
        
    def test_voucher_expires(self):
        self.assertField(
            field_name='expires_when',
            field_class=models.DateTimeField,
            must_not_have={'auto_now_add': True}
        )
