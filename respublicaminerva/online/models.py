from django.db import models
from django.contrib.auth.models import User
from auth.models import *

class MeasureType(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to="images/measure_types")

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        ordering = ['name']
        verbose_name = u'Тип мерки'
        verbose_name_plural = u'Типы мерок'

class Measure(models.Model):
    type = models.ForeignKey(MeasureType)
    comment = models.CharField(max_length=256)
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    
class EntryType(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __unicode__(self):
        return "%s - %s" % (self.start, self.end)

    class Meta:
        ordering = ['start']
        verbose_name = u'Часы приёма'
        verbose_name_plural = u'Часы приёма'

class UserEntry(models.Model):
    user = models.ForeignKey(User)
    type = models.ForeignKey(EntryType)
    date = models.DateField()
    description = models.CharField(max_length=256)
