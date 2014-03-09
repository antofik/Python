# coding=utf-8
from django.db import models
from cms.models.pluginmodel import CMSPlugin
from filer.fields.folder import FilerFolderField
from django.utils.translation import ugettext_lazy as _

class SlideshowPlugin(CMSPlugin):
    delay = models.IntegerField(default=5000, help_text=u'Задержка переключения фотографий, мс')
    show_weather = models.BooleanField(default=False, help_text=u'Показывать погодный модуль справа от слайдшоу')
    images = FilerFolderField(null=True, blank=True, default=None, verbose_name=_(u"Папка с картинками"))
