from django.urls import path, re_path

from . import views

urlpatterns = [
    path('layers', views.layer_handler, name="layers"),
    # path(r'clipper/app/(?P<app_name>[\d\w]+)$',
    #      views.clipper_remove_app, name='clipper_remove_app'),
    path('clipper/apps', views.clipper_get_all_app, name='clipper_apps'),
    # path('update_ckan', views.update_ckan, name='update_ckan'),
    # path('workflows', views.workflows, name='workflows'),

    path('clipper/predict/<str:model>',
         views.clipper_proxy, name='clipper_proxy'),
    path('projects', views.project, name="project"),
    path('folders', views.folder, name="folder"),
    path('files', views.files, name="files"),
    path('files/<str:id>', views.file_handler, name="files"),
]
