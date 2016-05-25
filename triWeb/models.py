from django.db import models

# Create your models here.

from django.db import models


class TestBedModel(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class DeviceModel(models.Model):
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    user = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    type = models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.name