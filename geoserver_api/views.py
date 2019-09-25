from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view


@csrf_exempt
def pipe_wms_to_geoserver(request, path=""):
    # TODO: implement authentication here
    layers = request.GET.get("layers", "")

    extra_requests_args = dict()
    remoteurl = 'http://geoserver:8080/geoserver/adalitix/wms'
    return proxy_view(request, remoteurl, extra_requests_args)


@csrf_exempt
def pipe_wcs_to_geoserver(request, path=""):
    # TODO: implement authentication here
    extra_requests_args = dict()
    remoteurl = 'http://geoserver:8080/geoserver/adalitix/wcs'
    return proxy_view(request, remoteurl, extra_requests_args)


@csrf_exempt
def pipe_ows_to_geoserver(request, path=""):
    # TODO: implement authentication here
    extra_requests_args = dict()
    remoteurl = 'http://geoserver:8080/geoserver/adalitix/ows'
    return proxy_view(request, remoteurl, extra_requests_args)
