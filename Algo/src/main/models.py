# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models import *
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class TagModel(models.Model):
    id = AutoField(primary_key=True)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    name = CharField(max_length=100, verbose_name=_(u"Tag"))

    def __unicode__(self):
        return self.name


class AlgorithmModel(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=256, verbose_name=_(u"Name"))
    authors = CharField(max_length=256, verbose_name=_(u"Authors"), blank=True)
    key = CharField(max_length=256, verbose_name=_(u"Access key"), blank=True)
    description = TextField(verbose_name=_(u"Description"), blank=True)
    verified = BooleanField(verbose_name=_(u"Verified"), blank=True, default=False)
    verification_request = BooleanField(verbose_name=_(u"Verification request"), blank=True, default=False)
    merge_request = BooleanField(verbose_name=_(u"Merge request"), blank=True, default=False)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    fork_of = ForeignKey('self', blank=True, null=True, related_name="forks", verbose_name=_("Forks"))
    tags = ManyToManyField(TagModel, related_name="algorithms", verbose_name=_(u"Tags"), blank=True)

    def __unicode__(self):
        return self.name


class LanguageModel(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=256, verbose_name=_(u"Name"))
    slug = SlugField()
    family = CharField(max_length=100)
    lexer = CharField(max_length=100)
    description = TextField(verbose_name=_(u"Description"), blank=True)
    example_code = TextField(verbose_name=_(u"Code example"), blank=True)
    is_dynamic = BooleanField(verbose_name=_(u"Is Dynamic"))
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    index = IntegerField(default=0, verbose_name=_(u"Order number"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-index', 'name']


class ImplementationModel(models.Model):
    id = AutoField(primary_key=True)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    algorithm = ForeignKey(AlgorithmModel, related_name="implementations", verbose_name=_("Algorithm"))
    language = ForeignKey(LanguageModel, related_name="implementations", verbose_name=_("Language"))
    source = TextField(verbose_name=_(u"Source"))
    accepted = BooleanField(default=True, verbose_name=_(u"Accepted"))

    def __unicode__(self):
        return u'%s. %s in %s' % (self.algorithm_id, self.algorithm, self.language)

    class Meta:
        ordering = ['algorithm', 'language']


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='my_profile')
    key = models.CharField(max_length=256, blank=True, default='', null=True)

    def __str__(self):
        return u"%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        if created:
            profile.save()

post_save.connect(create_user_profile, sender=User)

