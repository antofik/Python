# coding=utf-8
import os
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import  FileField, TextField, DateField, CharField
from django.utils.translation import ugettext_lazy as _
import settings


class Backup(models.Model):
    READY = "ready"
    CREATING = "creating"
    DELETED = "deleted"
    FAILED = "failed"
    STATUSES = (
        ('Готов', READY),
        ('Создаётся', CREATING),
        ('Удалён', DELETED),
        ('Ошибка', FAILED),
    )

    name = TextField(max_length=255)
    status = CharField(max_length=255, choices=STATUSES, default=CREATING)
    date = DateField(auto_now_add=True)
    data = CharField(max_length=255, verbose_name=_(u"Файл с бэкапом"))

    def __init__(self, *args, **kwargs):
        super(Backup, self).__init__(*args, **kwargs)

    def __unicode__(self):
        if self.name:
            return self.name
        if self.data:
            return self.data
        return ''

    @property
    def path(self):
        return os.path.join(settings.BACKUP_ROOT, self.data)

    @property
    def url(self):
        site = Site.objects.get_current()
        return 'http://' + site.domain + settings.BACKUP_URL + self.data