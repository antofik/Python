# coding=utf-8
from django.db import models
from django.db.models import OneToOneField
from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PageField
from cms.models import Page

class CMSRedirect(models.Model):
    page_from = OneToOneField(Page, unique=True, related_name="redirects_to", verbose_name=_("page"), blank=True, null=True)
    page_to = PageField(verbose_name=_("page"), related_name="redirects_from+", blank=True, null=True, help_text=_(u"Автоматически перенаправлять на эту страницу"))

    class Meta:
        verbose_name = _(u'Перенаправление')
        verbose_name_plural = _(u'Перенаправления')
