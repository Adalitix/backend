from django.db import models
import uuid


class Layer(models.Model):
    config = models.TextField(default='{}')


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    revision = models.ForeignKey(
        'Revision',
        on_delete=models.CASCADE,
    )
    file_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Revision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)  # comma separated tags
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.project.name + " - " + self.name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
