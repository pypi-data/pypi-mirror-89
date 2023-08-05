from django.db import models
from django.utils.translation import ugettext_lazy as _

from lostplaces.models.place import PlaceAsset

class ExternalLink(PlaceAsset):
    
    class Meta:
        abstract = True

    url = models.URLField(
        max_length=200,
        verbose_name=_('URL')
    )
    label = models.CharField(
        max_length=100,
        verbose_name=_('link text')
    )

class PhotoAlbum(ExternalLink):
    pass