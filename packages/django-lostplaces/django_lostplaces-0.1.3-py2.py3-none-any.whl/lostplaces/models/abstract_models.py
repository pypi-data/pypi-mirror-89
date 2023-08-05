
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from taggit.managers import TaggableManager

class Taggable(models.Model):
    '''
    This abstract model represtens an object that is taggable
    using django-taggit
    '''
    class Meta:
        abstract = True
        
    tags = TaggableManager(blank=True)
    
class Mapable(models.Model):
    '''
    This abstract model class represents an object that can be
    displayed on a map.
    '''
    class Meta:
        abstract = True
        
    name = models.CharField(
        max_length=50,
        verbose_name=_('Name'),
    )
    latitude = models.FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ],
        verbose_name=_('Latitude'),
        help_text=_('Latitude in decimal format: e. g. 41.40338')
    )
    longitude = models.FloatField(
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ],
        verbose_name=_('Longitude'),
        help_text=_('Longitude in decimal format: e. g. 2.17403')
    )

class Submittable(models.Model):
    '''
    This abstract model class represents an object that can be submitted by
    an explorer.
    '''
    class Meta:
        abstract = True

    submitted_when = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name=_('Submission date')
    )
    submitted_by = models.ForeignKey(
        'Explorer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)ss',
        verbose_name=_('Submitter')
    )

class Expireable(models.Model):
    """
    Base class for things that can expire, i.e. Vouchers
    """
    class Meta:
	    abstract = True
        
    created_when = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date')
    )
    expires_when = models.DateTimeField(
        verbose_name=_('Expiration date')
    )
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_when
