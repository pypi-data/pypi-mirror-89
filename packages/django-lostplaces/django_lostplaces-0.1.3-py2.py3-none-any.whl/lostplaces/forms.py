#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' (web)forms that can be used elsewhere. '''

from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from lostplaces.models import Place, PlaceImage, Voucher

class ExplorerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
    voucher = forms.CharField(
        max_length=30,
        help_text=_('The Voucher you got from an administrator')
    )

    def is_valid(self):
        super().is_valid()
        submitted_voucher = self.cleaned_data.get('voucher')
        try:
            fetched_voucher = Voucher.objects.get(code=submitted_voucher)
        except Voucher.DoesNotExist:
            self.add_error('voucher', _('Invalid voucher'))
            return False

        if not fetched_voucher.valid:
            self.add_error('voucher', _('Expired voucher'))
            return False

        fetched_voucher.delete()
        return True

class ExplorerChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        exclude = ['submitted_by']
        
class PlaceImageForm(forms.ModelForm):
    class Meta:
        model = PlaceImage
        fields = ['filename']
        widgets = {
            'filename': forms.ClearableFileInput(attrs={'multiple': True})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['filename'].required = False

class TagSubmitForm(forms.Form):
	tag_list = forms.CharField(
        max_length=500,
        required=False, 
        widget=forms.TextInput(attrs={'autocomplete':'off'})
        )
