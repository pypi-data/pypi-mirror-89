#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Classes and modules for the administrative backend. '''

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from lostplaces.models import *

from lostplaces.forms import ExplorerCreationForm, ExplorerChangeForm

# Register your models here.

class VoucherAdmin(admin.ModelAdmin):
    fields = ['code', 'expires_when', 'created_when']
    readonly_fields = ['created_when']
    list_display = ('__str__', 'code', 'created_when', 'expires_when', 'valid')

    def valid(self, instance):
        return timezone.now() <= instance.expires_when
    
    valid.boolean = True

class PhotoAlbumsAdmin(admin.ModelAdmin):
    list_display = ('label', 'place', 'url' )

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('name', 'submitted_by', 'submitted_when')

class PlaceImagesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'place', 'submitted_by')

admin.site.register(Explorer)
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(Place, PlacesAdmin)
admin.site.register(PlaceImage, PlaceImagesAdmin)
admin.site.register(PhotoAlbum, PhotoAlbumsAdmin)
