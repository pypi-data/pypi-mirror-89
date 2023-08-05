from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from lostplaces.views.base_views import PlaceAssetCreateView, PlaceAssetDeleteView
from lostplaces.models import PlaceImage, Place
from lostplaces.forms import PlaceImageForm

class MultiplePlaceImageUploadMixin:
    
    def handle_place_images(self, request, place):
        if request.FILES:
            submitted_by = request.user.explorer
            for image in request.FILES.getlist('filename'):
                place_image = PlaceImage.objects.create(
                    filename=image,
                    place=place,
                    submitted_by=submitted_by
                )
                place_image.save()
            
class PlaceImageCreateView(MultiplePlaceImageUploadMixin, PlaceAssetCreateView):
    model = PlaceImage
    form_class = PlaceImageForm
    template_name = 'place_image/place_image_create.html'
    success_message = _('Image(s) submitted successfully')
    commit = False

    def post(self, request, place_id, *args, **kwargs):
        self.place = get_object_or_404(Place, pk=place_id)
        self.handle_place_images(request, self.place)
        return redirect(self.get_success_url())
        
    def form_valid(self, form):
        form.instance.place = self.place
        form.instance.submitted_by = self.request.user.explorer
        return super().form_valid(form)
        
class PlaceImageDeleteView(PlaceAssetDeleteView):
    model = PlaceImage
    success_message = _('Image deleted successfully')
    permission_denied_message = _('You are not allowed to delete this image')
