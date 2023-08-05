#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
(Data)models which describe the structure of data to be saved into 
database.
'''

import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from lostplaces.models.abstract_models import Expireable

class Explorer(models.Model):
    """
    Profile that is linked to the a User.
    Every user has a profile.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='explorer'
    )

    def __str__(self):
        return self.user.username
        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Explorer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.explorer.save()

class Voucher(Expireable):
    """
    Vouchers are authorization to    created_when = models.DateTimeField(auto_now_add=True)
    expires_when = models.DateTimeField()kens to allow the registration of new users.
    A voucher has a code, a creation and a deletion date, which are all 
    positional. Creation date is being set automatically during voucher 
    creation. 
    """

    code = models.CharField(unique=True, max_length=30)
    
    @property
    def valid(self):
        return not self.is_expired

    def __str__(self):
        return "Voucher " + str(self.code)

