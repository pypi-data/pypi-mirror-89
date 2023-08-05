import os

from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from django.utils.translation import ugettext_lazy as _

from lostplaces.models.abstract_models import Submittable, Taggable, Mapable

from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

class Place(Submittable, Taggable, Mapable):
    """
    Place defines a lost place (location, name, description etc.).
    """

    location = models.CharField(
        max_length=50,
        verbose_name=_('Location'),
    )
    description = models.TextField(
        help_text=_('Description of the place: e.g. how to get there, where to be careful, the place\'s history...'),
        verbose_name=_('Description'),
    )

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'pk': self.pk})
    

    @classmethod
    # Get center position of LP-geocoordinates.
    def average_latlon(cls, place_list):
        amount = len(place_list)
        # Init fill values to prevent None
        longitude = 0
        latitude = 0

        if amount > 0:
            for place in place_list:
                longitude += place.longitude
                latitude += place.latitude
            return {'latitude':latitude / amount, 'longitude': longitude / amount}

        return {'latitude': latitude, 'longitude': longitude}

    def __str__(self):
        return self.name


def generate_image_upload_path(instance, filename):
    """
    Callback for generating path for uploaded images.
    Returns filename as: place_pk-placename{-rnd_string}.jpg
    """

    return 'places/' + str(instance.place.pk) + '-' + str(instance.place.name) + '.' + filename.split('.')[-1]

class PlaceAsset(Submittable):
    """
    Assets to a place, i.e. images
    """

    class Meta:
            abstract = True

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        null=True
    )

class PlaceImage (PlaceAsset):
    """
    PlaceImage defines an image file object that points to a file in uploads/.
    Intermediate image sizes are generated as defined in THUMBNAIL_ALIASES.
    PlaceImage references a Place to which it belongs.
    """

    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
    )
    filename = ThumbnailerImageField(
        upload_to=generate_image_upload_path, 
        resize_source=dict(size=(2560, 2560), 
        sharpen=True),
        verbose_name=_('Filename(s)'),
        help_text=_('Optional: One or more images to upload')
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='placeimages'
    )
    
    def __str__(self):
        """
        Returning the name of the corresponding place + id 
        of this image as textual representation of this instance
        """

        return 'Image ' + str(self.pk)


# These two auto-delete files from filesystem when they are unneeded:

@receiver(post_delete, sender=PlaceImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file (including thumbnails) from filesystem
    when corresponding `PlaceImage` object is deleted.
    """
    if instance.filename:
        # Get and delete all files and thumbnails from instance
        thumbmanager = get_thumbnailer(instance.filename)
        thumbmanager.delete(save=False)


@receiver(pre_save, sender=PlaceImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `PlaceImage` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = PlaceImage.objects.get(pk=instance.pk).filename
    except PlaceImage.DoesNotExist:
        return False

    # No need to delete thumbnails, as they will be overwritten on regeneration.
    new_file = instance.filename
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
