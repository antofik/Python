# coding=utf-8
import random
import threading
from multiprocessing import *
import time
import datetime
import traceback
import django
from django.db import connection
from django.utils.html import strip_tags
import sys
import gc
import objgraph
from webparser import parser, translator
from webparser.models import Category, Item, Image, get, db_product_failed, db_product, db_product_description
import re
from webparser.proxy import ProxyManager
import pprint

def parse_product(i):
    amount = 100
    print 'start %s' % i
    products = db_product.objects.all()[i*amount:(i+1)*amount]
    print 'selected %s items' % len(products)
    for product in products:
        try:
            id = product.product_id

            text = get(product.link, False)
            price = parser.get_value(r'"sku-price".*?>([^<]*?)</span>', text)
            if price:
                price = price.replace(',','')
            if price:
                price = float(price)
            else:
                price = 0
            product.price = price
            product.date_modified = datetime.datetime.now()
            product.save()

            bulk_price = parser.get_value(r'<span id="sku-bulk-price">\s*?(\S.*?\S)\s*?</dd>', text)
            if bulk_price:
                bulk_price = bulk_price.replace('</span>' ,'')

            description_en = db_product_description.objects.filter(product_id=id).get(language_id=2)
            description_en.bulk_price = bulk_price
            description_en.save()

            description_ru = db_product_description.objects.filter(product_id=id).get(language_id=1)
            description_ru.bulk_price = translator.translate(bulk_price)
            description_ru.save()

            print '[%s]+' % i
        except Exception, e:
            #print 'Error while parsing product %s %s %s' % (product.product_id, product.link, str(e))
            #traceback.print_exc()
            print '[%s]-' % i

class updater:
    concurrent_threads = 300
    concurrent_products = 1

    def __init__(self):
        self.categories = []
        self.done = True

    def update_costs(self):
        self.done = False
        result = []
        ProxyManager.initialize()

        self.lock = threading.Semaphore(self.concurrent_threads)
        threads = []
        amount = 100

        #pool = Pool()
        #pool.map(parse_product, range(300), chunksize=1)
        #if True:
        #    return
        for i in xrange(self.concurrent_threads):
            products = db_product.objects.all()[i*amount:(i+1)*amount]
            print 'Launching new thread %s with %s products' % (i, len(products))
            th = threading.Thread(target=self.parse_category, args=(products,i,))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()

        self.done = True
        print 'Updating finished'
        return result

    def parse_category(self, products, number):
        self.lock.acquire()
        try:
            for product in products:
                try:
                    id = product.product_id

                    text = get(product.link, False)
                    price = parser.get_value(r'"sku-price".*?>([^<]*?)</span>', text)
                    if price:
                        price = price.replace(',','')
                    if price:
                        price = float(price)
                    else:
                        price = 0
                    product.price = price
                    product.date_modified = datetime.datetime.now()
                    product.save()

                    bulk_price = parser.get_value(r'<span id="sku-bulk-price">\s*?(\S.*?\S)\s*?</dd>', text)
                    if bulk_price:
                        bulk_price = bulk_price.replace('</span>' ,'')

                    description_en = db_product_description.objects.filter(product_id=id).get(language_id=2)
                    description_en.bulk_price = bulk_price
                    description_en.save()

                    description_ru = db_product_description.objects.filter(product_id=id).get(language_id=1)
                    description_ru.bulk_price = translator.translate(bulk_price)
                    description_ru.save()

                    print '[%s]+' % number
                except Exception, e:
                    #print 'Error while parsing product %s %s %s' % (product.product_id, product.link, str(e))
                    #traceback.print_exc()
                    print '[%s]-' % number
                    pass
        except Exception, e:
            print 'Error while parsing category: %s' % str(e)
            traceback.print_exc()
            pass
        self.lock.release()
        connection.close()

class watch:
    def __init__(self):
        self.times = []
        self.deltas = []
        self.measure()

    def measure(self):
        t = datetime.datetime.now()
        if self.times:
            p = self.times[-1:][0]
            delta = (t - p).total_seconds()
            self.deltas.append(delta)
        self.times.append(t)

    def show(self):
        print 'Watch report'
        for d in self.deltas:
            print '  - %s' % d


