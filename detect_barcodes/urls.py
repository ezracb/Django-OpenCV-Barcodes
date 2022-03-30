from django.urls import path

from . import views

urlpatterns = [
    path('', views.detect, name='detect_barcodes'),
    path('camera_feed', views.camera_feed, name='camera_feed'),
    path('camera_feed_1', views.camera_feed_1, name='camera_feed_1'),
]
