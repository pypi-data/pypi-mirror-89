#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from lostplaces.views import (
    HomeView, 
    PlaceDetailView, 
    PlaceListView, 
    PlaceCreateView,
    PlaceUpdateView,
    PlaceDeleteView,
    PlaceTagDeleteView,
	PlaceTagSubmitView,
	PhotoAlbumCreateView,
	PhotoAlbumDeleteView,
    PlaceImageCreateView,
    PlaceImageDeleteView,
    FlatView,
    ExplorerProfileView
)

urlpatterns = [
    path('', HomeView.as_view(), name='lostplaces_home'),
    path('place/<int:pk>/', PlaceDetailView.as_view(), name='place_detail'),
    path('place/create/', PlaceCreateView.as_view(), name='place_create'),
	path('photo_album/create/<int:place_id>', PhotoAlbumCreateView.as_view(), name='photo_album_create'),
	path('photo_album/delete/<int:pk>', PhotoAlbumDeleteView.as_view(), name='photo_album_delete'),
    path('place/update/<int:pk>/', PlaceUpdateView.as_view(), name='place_edit'),
    path('place/delete/<int:pk>/', PlaceDeleteView.as_view(), name='place_delete'),
    path('place/', PlaceListView.as_view(), name='place_list'),
    path('place_image/create/<int:place_id>', PlaceImageCreateView.as_view(), name='place_image_create'),
    path('place_image/delete/<int:pk>', PlaceImageDeleteView.as_view(), name='place_image_delete'),
    path('flat/<slug:slug>/', FlatView, name='flatpage'),

    # POST-only URLs for tag submission
	path('place/tag/<int:tagged_id>', PlaceTagSubmitView.as_view(), name='place_tag_submit'),
    path('place/tag/delete/<int:tagged_id>/<int:tag_id>', PlaceTagDeleteView.as_view(), name='place_tag_delete'),
    
    path('explorer/<int:explorer_id>/', ExplorerProfileView.as_view(), name='explorer_profile')
]
