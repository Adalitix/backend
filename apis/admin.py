from django.contrib import admin
from .models import Layer, File, Folder, Project


class LayerAdmin(admin.ModelAdmin):
    list_display = ("config", "id")


class FileAdmin(admin.ModelAdmin):
    list_display = ("name", "folder", "id")
    fields = ("name", "folder", "file", "file_type")


class FolderAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "project", "id")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


admin.site.register(Layer, LayerAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Project, ProjectAdmin)
