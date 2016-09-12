# -*- coding: utf-8 -*-
from django.db import models
from django.core.files.storage import FileSystemStorage, Storage
from django.conf import settings
import os

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        return name
    def _save(self, name, content):
        if self.exists(name):
            raise Exception("File with the same name already exist.. Please delete it and re-upload the File")
        return super(OverwriteStorage, self)._save(name, content)

class Stream(models.Model):
    StreamName = models.FileField(storage=OverwriteStorage())
    #StreamName = models.FileField()
    StreamType = models.CharField(max_length=100)
    EncodedStreamType = models.CharField(default="Not set",max_length=100)
    RawStreamType = models.CharField(default="Not set",max_length=100)
    Resolution = models.CharField(default="Not set",max_length=100)
    Frames = models.CharField(default="Not set",max_length=100)
    ScanType = models.CharField(default="Not set",max_length=100)
    Complexity = models.CharField(default="Not set",max_length=100)
    FrameCount = models.CharField(default="Not set",max_length=100)
    Conformance = models.CharField(default="Not set",max_length=100)
    ContainerFormat = models.CharField(default="Not set",max_length=100)
    Source = models.CharField(default="Not set",max_length=100)