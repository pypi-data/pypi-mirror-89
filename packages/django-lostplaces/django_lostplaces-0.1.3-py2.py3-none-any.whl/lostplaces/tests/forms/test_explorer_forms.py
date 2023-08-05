import datetime

from django import forms
from django.utils import timezone

from lostplaces.tests.forms import FormTestCase
from lostplaces.forms import ExplorerCreationForm
from lostplaces.models.models import Voucher

class ExplorerCreationFormTestCase(FormTestCase):
    """
    This test case only tests for the voucher since all other aspects don't realy matter
    to this project and are already tested by django
    """
    form = ExplorerCreationForm
    
    @classmethod
    def setUpTestData(cls):
        Voucher.objects.create(
            code='Imacode123',
            expires_when=timezone.now() + datetime.timedelta(minutes=1)
        )
    
    def setUp(self):
        self.post_data = {
            'voucher': 'Imacode123',
            'username': 'testpeter',
            'email': 'testpeter@example.org',
            'password1': 'Develop123',
            'password2': 'Develop123'
        }
    
    def test_voucher_field(self):
        self.assertField(
            field_name='voucher',
            field_class=forms.CharField
        )
        
    def test_validation_valid(self):
        form = ExplorerCreationForm(self.post_data)
        self.assertTrue(
            form.is_valid(),
            msg='Expecting the %s to validate' % (
                self.form.__name__
            )
        )
        
    def test_validation_invalid(self):
        self.post_data = {
            'voucher': 'Imanotacode123'
        }
        form = ExplorerCreationForm(self.post_data)
        self.assertFalse(
            form.is_valid(),
            msg='Expecting the %s to not validate' % (
                self.form.__name__
            )
        )
    