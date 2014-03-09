# coding=utf-8
import os
from pprint import pprint
import uuid
import datetime
from django.db import models, connection, transaction, IntegrityError
from Electrosha import settings
from webparser import http, translator, parser
import warnings
from django.core.exceptions import ObjectDoesNotExist
from webparser.http import loader
import traceback
from clint.textui import colored
import random

warnings.filterwarnings("ignore", ".* default value")
warnings.filterwarnings("ignore", ".* time zone support is active")
warnings.filterwarnings("ignore", "Data truncated .*")

def dump(obj, len = 10):
    '''return a printable representation of an object for debugging'''
    if len<=0:
        return '...'
    newobj=obj
    if '__dict__' in dir(obj):
        newobj=obj.__dict__
        if ' object at ' in str(obj) and not newobj.has_key('__type__'):
            newobj['__type__']=str(obj)
        for attr in newobj:
            newobj[attr]=dump(newobj[attr], len - 1)
    return newobj

provider = loader(loader.defaultHost)
def get(url, save = True):
    if url.startswith('/'):
        url = loader.defaultHost + url
    if not url.startswith('http://www.aliexpress.com/cross-domain/freight'):
        url = url.lower()
    #print 'get', url
    if save:
        data = getCache(url)
        if data:
            print 'cache success'
            return data
    data = provider.get(url)
    if save:
        saveCache(url, data)
    return data

def saveCache(link, html):
    item = html_cache()
    item.link = link
    item.html = html
    item.save()
    del item
    connection.close()

def getCache(url):
    data = html_cache.objects.filter(link=url).all()[:1]
    value = data[0].html if data else None
    del data
    connection.close()
    return value


def clear_db():
    if True:
        return
    cursor = connection.cursor()
    #cursor.execute("delete from html_cache")
    cursor.execute("delete from product_failed")
    #cursor.execute("delete from category")
    #cursor.execute("delete from category_description")
    #ursor.execute("delete from category_to_store")
    cursor.execute("delete from product")
    cursor.execute("delete from product_to_category")
    cursor.execute("delete from product_to_store")
    cursor.execute("delete from product_image")
    cursor.execute("delete from product_gallery")
    cursor.execute("delete from product_description")
    cursor.execute("delete from attribute")
    cursor.execute("delete from attribute_description")
    cursor.execute("delete from product_attribute")
    transaction.commit_unless_managed()

class html_cache(models.Model):
    link = models.CharField(max_length=1024)
    html = models.TextField()
    class Meta:
        db_table = 'html_cache'

class db_category(models.Model):
    category_id = models.IntegerField(default=0, primary_key=True)
    parent_id = models.IntegerField(default=0)
    status = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'category'

class db_category_description(models.Model):
    category_id = models.IntegerField()
    language_id = models.IntegerField()
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'category_description'

class db_category_to_store(models.Model):
    category_id = models.IntegerField(primary_key=True)
    store_id = models.IntegerField(default=0)
    class Meta:
        db_table = 'category_to_store'

class db_product(models.Model):
    product_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=64, default='no model')
    quantity = models.IntegerField(default=10)
    pieces = models.IntegerField(null=True)
    link = models.CharField(max_length=512, null=True)
    image = models.CharField(max_length=255, null=True)
    price = models.FloatField()
    shipping_price = models.FloatField(default=0)
    date_added = models.DateTimeField()
    date_modified = models.DateTimeField()
    status = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'product'

class db_product_failed(models.Model):
    product_id = models.IntegerField()
    category_id = models.IntegerField()
    link = models.CharField(max_length=1024)
    error = models.CharField(max_length=1024)
    class Meta:
        db_table = 'product_failed'

class db_product_to_category(models.Model):
    product_id = models.IntegerField()
    category_id = models.IntegerField()
    class Meta:
        db_table = 'product_to_category'

class db_product_to_store(models.Model):
    product_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'product_to_store'

class db_product_image(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    image = models.CharField(max_length=255)
    class Meta:
        db_table = 'product_image'

class db_product_gallery(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    image = models.CharField(max_length=255)
    class Meta:
        db_table = 'product_gallery'

class db_product_description(models.Model):
    product_id = models.IntegerField()
    language_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    meta_description = models.CharField(max_length=255)
    meta_keyword = models.CharField(max_length=255)
    pieces = models.CharField(max_length=255)
    bulk_price = models.CharField(max_length=255)
    shipping_time = models.CharField(max_length=255)
    class Meta:
        db_table = 'product_description'

class db_attribute(models.Model):
    attribute_id = models.AutoField(primary_key=True)
    attribute_group_id = models.IntegerField(default=1)
    class Meta:
        db_table = 'attribute'

class db_attribute_description(models.Model):
    attribute_id = models.IntegerField()
    language_id = models.IntegerField()
    name = models.CharField(max_length=64)
    class Meta:
        db_table = 'attribute_description'

class db_product_attribute(models.Model):
    product_id = models.IntegerField()
    attribute_id = models.IntegerField()
    language_id = models.IntegerField()
    text = models.TextField()
    class Meta:
        db_table = 'product_attribute'

############################################
### Logic objects ##########################
############################################

class Category():
    def __init__(self, link, name):
        self.link = link
        self.name = name
        self.name_ru = None
        self.categories = []
        self.items = []
        self.id = parser.get_value(r'category/(\d+?)/', self.link)
        print 'category:', self.id

    def addCategory(self, link, name):
        category = Category(link, name)
        self.categories.append(category)

    def save(self, parent_id = 0):
        if db_category.objects.filter(category_id=self.id).exists():
            print 'category exists', self.id
            return
        print 'Saving new category', self.name

        self.name_ru = translator.translate(self.name).strip()

        parent = db_category()
        parent.category_id = self.id
        parent.parent_id = parent_id
        parent.save()

        to_store = db_category_to_store()
        to_store.category_id = self.id
        to_store.save()

        parent_desc = db_category_description()
        parent_desc.language_id = 2
        parent_desc.category_id = parent.category_id
        parent_desc.name = self.name
        parent_desc.save()

        parent_desc2 = db_category_description()
        parent_desc2.language_id = 1
        parent_desc2.category_id = parent.category_id
        parent_desc2.name = self.name_ru
        parent_desc2.save()

        connection.close()

        for child in self.categories:
            child.save(parent.category_id)

class Item:
    def __init__(self, link, name):
        self.link = link
        self.name = name
        self.loaded = False
        self.images = []
        self.gallery = []
        self.image = None
        self.id = None
        self.price = None
        self.pieces = None
        self.discount = None
        self.discounttime = None
        self.specifics = None
        self.packaging = None
        self.shipping = None
        self.information_en = None
        self.information_ru = None

    def addImage(self, link):
        image = Image(link)
        self.images.append(image)

    def save(self, category_id):
        if db_product.objects.filter(product_id=self.id).exists():
            print 'product exists', self.id
            connection.close()
            return
        #print 'Saving new product...'
        start = datetime.datetime.now()

        item = db_product()
        item.product_id = self.id
        item.image = self.image.local
        item.price = self.price.replace(',','') if self.price else 0
        item.pieces = self.pieces or 0
        item.link = loader.defaultHost + self.link
        item.shipping_price = self.shipping.replace(',','') if self.shipping else 0
        item.date_added = datetime.datetime.now()
        item.date_modified = datetime.datetime.now()
        item.save()
        #pprint(dump(item))

        to_category = db_product_to_category()
        to_category.category_id = category_id
        to_category.product_id = item.product_id
        to_category.save()

        to_store = db_product_to_store()
        to_store.product_id = item.product_id
        to_store.save()

        for image in self.images:
            to_image = db_product_image()
            to_image.image = image.local
            to_image.product_id = item.product_id
            to_image.save()

        for image in self.gallery:
            to_gallery = db_product_gallery()
            to_gallery.image = image.local
            to_gallery.product_id = item.product_id
            to_gallery.save()

        print colored.green('ping')
        i = 0
        try:
            desc_en = db_product_description()
            desc_en.product_id = item.product_id
            desc_en.id = random.randint(100000,10000000)
            desc_en.language_id = 2
            desc_en.description = self.information_en or 'No description'
            desc_en.meta_description = self.description_en
            desc_en.meta_keyword = self.keywords_en
            desc_en.name = self.name
            desc_en.pieces = self.pieces_text_en
            desc_en.bulk_price = str(self.bulk_price_en)
            desc_en.shipping_time = self.shipping_time
            i += 1
        except Exception, e:
            print colored.yellow('X'*10000)
            traceback.print_exc()

        try:
            desc_ru = db_product_description()
            desc_ru.id = random.randint(100000,10000000)
            desc_ru.product_id = item.product_id
            desc_ru.language_id = 1
            desc_ru.description = self.information_ru or 'Без описания'
            desc_ru.meta_description = self.description_ru
            desc_ru.meta_keyword = self.keywords_ru
            desc_ru.name = translator.translate(self.name)
            desc_ru.pieces = self.pieces_text_ru
            desc_ru.bulk_price = self.bulk_price_ru
            desc_ru.shipping_time = self.shipping_time
            desc_ru.save()
            i += 1
            desc_en.save()
        except Exception, e:
            print colored.red('X'*8000)
            traceback.print_exc()
            
        if i<2:
            print colored.green('Oo'*10000)
        i = 0
        for el in self.specifics:
            if len(self.specifics_ru)>i:
                el_ru = self.specifics_ru[i]
            else:
                el_ru = el

            name = el[0].strip()
            try:
                attr_desc = db_attribute_description.objects.filter(language_id=2).get(name=name)
                attr = db_attribute.objects.get(attribute_id=attr_desc.attribute_id)
            except:
                attr_desc = None
                attr = None

            name_ru = el_ru[0].strip() if len(el_ru)>0 else name
            try:
                attr_desc_ru = db_attribute_description.objects.filter(language_id=1).get(name=name_ru)
            except:
                attr_desc_ru = None

            if not attr:
                attr = db_attribute()
                attr.attribute_group_id = 1
                attr.save()

            if not attr_desc:
                try:
                    attr_desc = db_attribute_description()
                    attr_desc.language_id = 2
                    attr_desc.attribute_id = attr.attribute_id
                    attr_desc.name = el[0]
                    attr_desc.save()
                except IntegrityError, e:
                    pass

            if not attr_desc_ru:
                try:
                    attr_desc_ru = db_attribute_description()
                    attr_desc_ru.language_id = 1
                    attr_desc_ru.attribute_id = attr.attribute_id
                    attr_desc_ru.name = name_ru
                    attr_desc_ru.save()
                except IntegrityError, e:
                    pass

            try:
                attr_val = db_product_attribute()
                attr_val.attribute_id = attr.attribute_id
                attr_val.language_id = 2
                attr_val.text = el[1]
                attr_val.product_id = item.product_id
                attr_val.save()
            except IntegrityError, e:
                pass

            try:
                attr_val = db_product_attribute()
                attr_val.attribute_id = attr.attribute_id
                attr_val.language_id = 1
                attr_val.text = el_ru[1] if len(el_ru)>1 else el[1]
                attr_val.product_id = item.product_id
                attr_val.save()
            except IntegrityError, e:
                pass


            i += 1

        connection.close()
        delta = (datetime.datetime.now() - start).total_seconds()
        #print 'Product saved in %s seconds' % delta

class Image:
    loader = http.loader("www.aliexpress.com")

    def __init__(self, link):
        self.link = link
        self.loaded = False
        self.error = False
        self.local = ''

    def download(self):
        filename = '%s.jpg' % str(uuid.uuid4())
        self.local = 'parsed/%s' % str(filename)
        path = os.path.abspath('./media/userimages/' + filename)
        try:
            self.loader.save(self.link, path)
        except:
            self.error = True
        self.loaded = True
