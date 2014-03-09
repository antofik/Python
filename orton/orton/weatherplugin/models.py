# coding=utf-8
from cmsplugin_filer_image.models import FilerImage
from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.db.models import ManyToManyField
from filer.fields.folder import FilerFolderField
from filer.fields.image import FilerImageField
from django.utils.translation import ugettext_lazy as _

class Weather(CMSPlugin):
    width = models.IntegerField(default=250, help_text=u'Ширина модуля в пикселях')
