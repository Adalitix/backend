from django.contrib import admin
from .models import Layer, File, Revision, Project


class LayerAdmin(admin.ModelAdmin):
    list_display = ("config", "id")


class FileAdmin(admin.ModelAdmin):
    list_display = ("name", "revision", "id")


class RevisionAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "tags", "id")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


admin.site.register(Layer, LayerAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Revision, RevisionAdmin)
admin.site.register(Project, ProjectAdmin)
