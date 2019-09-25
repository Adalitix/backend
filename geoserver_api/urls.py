from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path('adalitix/wms', views.pipe_wms_to_geoserver),
    re_path('adalitix/wcs', views.pipe_wcs_to_geoserver),
    re_path('adalitix/ows', views.pipe_ows_to_geoserver),
]
