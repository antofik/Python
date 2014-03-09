from django.db import models

class DancerEmail(models.Model):
    source = models.CharField(max_length=128)
    raw = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    data = models.TextField()
    processed = models.BooleanField(default=False)

class DancerPhone(models.Model):
    source = models.CharField(max_length=128)
    raw = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    data = models.TextField()
    processed = models.BooleanField(default=False)
