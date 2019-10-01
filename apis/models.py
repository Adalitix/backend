from django.db import models
import uuid


class Layer(models.Model):
    config = models.TextField(default='{}')


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(
        'Folder',
        on_delete=models.CASCADE,
    )
    file_type = models.CharField(max_length=100)
    file = models.FileField(
        blank=True,
        null=True,
        upload_to="uploaded_data"
    )

    def __str__(self):
        return self.name


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'Folder',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.parent.name + " - " + self.name if self.parent is not None else self.name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
