# coding=utf-8
from cms.models.fields import PageField
import dbsettings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import CharField, IntegerField, TextField, BooleanField, ForeignKey, DateTimeField, ManyToManyField, AutoField, DateField, URLField, OneToOneField
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from django.utils.translation import ugettext_lazy as _

class SocialOptions(dbsettings.Group):
    use_vkontakte = dbsettings.BooleanValue(u"Использовать Вконтакте")
    url_vkontakte = dbsettings.StringValue(u"Вконтакте")

    use_facebook = dbsettings.BooleanValue(u"Использовать Facebook")
    url_facebook = dbsettings.StringValue(u"Facebook")

    use_odnoklassniki = dbsettings.BooleanValue(u"Использовать Одноклассники")
    url_odnoklassniki = dbsettings.StringValue(u"Одноклассники")

    use_moimir = dbsettings.BooleanValue(u"Использовать Мой мир")
    url_moimir = dbsettings.StringValue(u"Мой мир")

options = SocialOptions()

class CatalogCategoryModel(models.Model):
    name = CharField(max_length=120, verbose_name=_(u"Короткое название"))
    full_name = CharField(max_length=256, null=True, verbose_name=_(u"Полное название)"))
    parent = ForeignKey('self', related_name="children", null=True, blank=True, verbose_name=_(u"Родительская категория"), limit_choices_to={"parent__isnull":True}, on_delete=models.SET_NULL)
    orderindex = IntegerField(default=0, blank=True, null=False, verbose_name=_(u"Порядковый номер"))
    description = TextField(blank=True, verbose_name=_(u"Описание"))
    description_page = PageField(related_name="linked_catalog_category+", null=True, blank=True, verbose_name=_(u"Страница помощи"))

    def __init__(self, *args, **kwargs):
        super(CatalogCategoryModel, self).__init__(*args, **kwargs)
        self.full_view = True

    def get_absolute_url(self):
        if self.parent:
            return reverse(u'catalog.views.subcategory', args=[unicode(self.name)])
        return reverse(u'catalog.views.category', args=[unicode(self.name)])

    def __unicode__(self):
        if not self.parent:
            return self.name
        else:
            return u"%s => %s" % (unicode(self.parent), self.name)

    def get_absolute_url(self):
        if self.full_view:
            return reverse(u'catalog.views.category', args=[unicode(self.name)])
        else:
            return reverse(u'catalog.views.image_category', args=[unicode(self.name)])

    class Meta:
        ordering = ['orderindex', 'name']
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class CatalogItemModel(models.Model):
    ACTIVE_SUBSTANCES = ((u"д.в.", u"д.в."),(u"в %", u"в %"))

    name = CharField(max_length=120, verbose_name=_(u"Название"))
    category = ForeignKey(CatalogCategoryModel, related_name="items", verbose_name=_(u"Категория"))#uncomment to allow items in subcategories only: limit_choices_to={"parent__isnull":False})
    purpose = TextField(verbose_name=_(u"Назначение"))
    action = TextField(verbose_name=_(u"Действие"))
    usage = TextField(verbose_name=_(u"Применение"))
    active_substance = CharField(max_length=64, choices=ACTIVE_SUBSTANCES, default=ACTIVE_SUBSTANCES[0][0], verbose_name=_(u"Тип действующего вещества"))
    chemical = TextField(verbose_name=_(u"Действующее вещество"))
    image = FilerImageField(null=True, blank=True, default=None, verbose_name=_(u"Фотография препарата"), on_delete=models.SET_NULL)
    image_small = FilerImageField(null=True, blank=True, default=None, related_name="catalogitem_image_small+", verbose_name=_(u"Альтернативная фотография препарата"), on_delete=models.SET_NULL)
    description_image = FilerImageField(null=True, blank=True, default=None, verbose_name=_(u"Фотография описания"), related_name="description_image+", on_delete=models.SET_NULL)
    orderindex = IntegerField(default=0, blank=True, null=False, verbose_name=_(u"Порядковый номер"))
    show_on_main_page = BooleanField(default=True, verbose_name=_(u"Показывать на главной странице"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(u'catalog.views.item', args=[unicode(self.name)])

    @property
    def main_category(self):
        parent = self.category
        while parent.parent:
            parent = parent.parent
        return parent

    class Meta:
        ordering = ['name']
        verbose_name = u'Препарат'
        verbose_name_plural = u'Препараты'


class CatalogVideoModel(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=120, verbose_name=_(u"Название"))
    description = TextField(verbose_name=_(u"Описание"), blank=True)
    date_added = DateTimeField(auto_now_add=True)
    youtube = URLField(verbose_name=_(u"Ссылка на видео в Youtube"), help_text=_(u"Пример: http://www.youtube.com/watch?v=g9d49Mw-Bus"), blank=True)

    video = FilerFileField(verbose_name=_('movie file'), help_text=_('use .flv file or h264 encoded video file'), blank=True, null=True, on_delete=models.SET_NULL)
    image = FilerImageField(verbose_name=_('image'), help_text=_('preview image file'), null=True, blank=True, related_name='catalog_video_image+', on_delete=models.SET_NULL)

    items = ManyToManyField(CatalogItemModel, blank=True, related_name="videos", db_table="CatalogItemVideoModel", help_text=_(u"Связанные препараты"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(u'catalog.views.video_item', args=[unicode(self.id)])

    def get_absolute_url_of_list(self):
        return reverse(u'catalog.views.video_catalog')

    def youtube_url(self):
        return self.youtube.replace('/watch?v=', '/embed/')

    class Meta:
        ordering = ['-date_added']
        verbose_name = u'Видеоматериал'
        verbose_name_plural = u'Видеоматериалы'


class CatalogArticleModel(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=120, verbose_name=_(u"Название"))
    image = FilerImageField(verbose_name=_('image'), help_text=_('preview image file'), null=True, blank=True, related_name='catalog_article_image+', on_delete=models.SET_NULL)
    short_description = TextField(max_length=80, verbose_name=_(u"Краткое описание"))
    description = TextField(verbose_name=_(u"Статья"))
    date_added = DateField(verbose_name=_(u"Дата выпуска"))
    author = ForeignKey(User, editable=False)

    items = ManyToManyField(CatalogItemModel, blank=True, related_name="articles", db_table="catalog_article_to_item", help_text=_(u"Связанные препараты"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(u'catalog.views.articles_item', args=[unicode(self.id)])

    def get_absolute_url_of_list(self):
        return reverse(u'catalog.views.articles_list')

    class Meta:
        ordering = ['-date_added']
        verbose_name = u'Статья'
        verbose_name_plural = u'Статьи'


class CatalogNewsModel(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=120, verbose_name=_(u"Название"))
    image = FilerImageField(verbose_name=_('image'), help_text=_('preview image file'), null=True, blank=True, related_name='catalog_news_image+', on_delete=models.SET_NULL)
    short_description = TextField(max_length=80, verbose_name=_(u"Краткое описание"))
    description = TextField(verbose_name=_(u"Текст новости"))
    date_added = DateTimeField(verbose_name=_(u"Дата выпуска"))
    author = ForeignKey(User, editable=False)

    items = ManyToManyField(CatalogItemModel, blank=True, related_name="news", db_table="catalog_news_to_item", help_text=_(u"Связанные препараты"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(u'catalog.views.news_item', args=[unicode(self.id)])

    def get_absolute_url_of_list(self):
        return reverse(u'catalog.views.news_list')

    class Meta:
        ordering = ['-date_added']
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'


class CatalogAdviceModel(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=120, verbose_name=_(u"Название"))
    image = FilerImageField(verbose_name=_('image'), help_text=_('preview image file'), null=True, blank=True, related_name='catalog_advice_image+', on_delete=models.SET_NULL)
    short_description = TextField(max_length=80, verbose_name=_(u"Краткое описание"))
    description = TextField(verbose_name=_(u"Совет"))
    date_added = DateField(verbose_name=_(u"Дата выпуска"))
    author = ForeignKey(User, editable=False)

    items = ManyToManyField(CatalogItemModel, blank=True, related_name="advices", db_table="catalog_advice_to_item", help_text=_(u"Связанные препараты"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(u'catalog.views.advices_item', args=[unicode(self.id)])

    def get_absolute_url_of_list(self):
        return reverse(u'catalog.views.advices_list')

    class Meta:
        ordering = ['-date_added']
        verbose_name = u'Совет'
        verbose_name_plural = u'Советы'

class FeedbackOptions(dbsettings.Group):
    emails = dbsettings.StringValue(u"Список email-ов для обратной связи, через запятую")

class FeedbackModel(models.Model):
    name = CharField(max_length=120, verbose_name=_(u"Имя"))
    phone = CharField(max_length=120, verbose_name=_(u"Телефон"))
    comment = TextField(verbose_name=_(u"Комментарий"))
    recall = BooleanField(default=False, verbose_name=_(u"Перезвонить"))
    date_added = DateTimeField(auto_now_add=True)

    options = FeedbackOptions()

    def __unicode__(self):
        return u"%s %s %s[%s]:\t%s" % (self.recall and u"Перезвонить!" or "", self.date_added.date(), self.name, self.phone, self.comment[:50])

    class Meta:
        ordering = ['-date_added']
        verbose_name = u'Запрос обратной связи'
        verbose_name_plural = u'Запросы обратной связи'


class PartnerModel(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=120, verbose_name=_(u"Название партнёра"))
    url = URLField(max_length=256, verbose_name=_(u"Адрес партнёра"))
    image = FilerImageField(verbose_name=_('image'), help_text=_(u'Логотип партнёра'), null=True, blank=True, related_name='catalog_partner_image+', on_delete=models.SET_NULL)
    description = TextField(verbose_name=_(u"Описание", blank=True))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = u'Партнёр'
        verbose_name_plural = u'Партнёры'


class DocumentModel(models.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=120, verbose_name=_(u"Название документа"))
    doc = FilerFileField(verbose_name=_(u'Word'), help_text=_(u'Word документ'), null=True, blank=True, related_name='catalog_document_doc+', on_delete=models.SET_NULL)
    pdf = FilerFileField(verbose_name=_(u'PDF'), help_text=_(u'PDF документ'), null=True, blank=True, related_name='catalog_document_pdf+', on_delete=models.SET_NULL)
    xls = FilerFileField(verbose_name=_(u'Excel'), help_text=_(u'Excel документ'), null=True, blank=True, related_name='catalog_document_xls+', on_delete=models.SET_NULL)
    rar = FilerFileField(verbose_name=_(u'Архив'), help_text=_(u'Архивированный документ'), null=True, blank=True, related_name='catalog_document_rar+', on_delete=models.SET_NULL)
    img = FilerImageField(verbose_name=_(u'Картинка'), help_text=_(u'Документ в виде картинки jpg, png, bmp'), null=True, blank=True, related_name='catalog_document_img+', on_delete=models.SET_NULL)
    description = TextField(verbose_name=_(u"Описание", help_text=_(u'Описание'), blank=True))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u'Документ'
        verbose_name_plural = u'Документы'


class CalendarModel(models.Model):
    id = AutoField(primary_key=True)
    item = OneToOneField(CatalogItemModel, unique=True, related_name="calendar", verbose_name=_(u"Календарь"))
    m1 = CharField(max_length=255, verbose_name=_(u"Январь"), blank=True)
    m2 = CharField(max_length=255, verbose_name=_(u"Февраль"), blank=True)
    m3 = CharField(max_length=255, verbose_name=_(u"Март"), blank=True)
    m4 = CharField(max_length=255, verbose_name=_(u"Апрель"), blank=True)
    m5 = CharField(max_length=255, verbose_name=_(u"Май"), blank=True)
    m6 = CharField(max_length=255, verbose_name=_(u"Июнь"), blank=True)
    m7 = CharField(max_length=255, verbose_name=_(u"Июль"), blank=True)
    m8 = CharField(max_length=255, verbose_name=_(u"Август"), blank=True)
    m9 = CharField(max_length=255, verbose_name=_(u"Сентябрь"), blank=True)
    m10 = CharField(max_length=255, verbose_name=_(u"Октябрь"), blank=True)
    m11 = CharField(max_length=255, verbose_name=_(u"Ноябрь"), blank=True)
    m12 = CharField(max_length=255, verbose_name=_(u"Декабрь"), blank=True)

    def monthes(self):
        return [self.m1, self.m2, self.m3, self.m4,
                self.m5, self.m6, self.m7, self.m8,
                self.m9, self.m10, self.m11, self.m12]

    def __unicode__(self):
        return self.item.name

    class Meta:
        verbose_name = u'Календарь'
        verbose_name_plural = u'Календари'
