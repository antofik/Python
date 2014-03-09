# coding=utf-8
import random
import threading
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
from webparser.models import Category, Item, Image, get, db_product_failed, db_product
import re
from webparser.proxy import ProxyManager
import pprint

class aliexpress:
    concurrent_threads = 300
    concurrent_products = 1
    done_count = 0

    parsed_category = []

    main_category_match = re.compile(r'\s*<a.*?class="main-category".*>.*</a>\s*')
    main_category_regex = re.compile(r'\s*<a.*href="http://www.aliexpress.com(/category/(?:[^"]*))"[^<>]*>(.*)</a>\s*')
    category_regex = re.compile(r'.*<a\s*?href="http://www.aliexpress.com(/category/(?:[^"]*))">(.*)</a></li>.*')
    item_regex = re.compile(r'''<a\s*?class="history-item product"\s*?href="http://www.aliexpress.com(/item/(?:[^"]*))"\s*?title="([^"]*)"''')

    def __init__(self):
        self.categories = []
        self.done = True

    def parse(self):
        self.done = False
        result = []
        ProxyManager.initialize()
        text = get('/all-wholesale-products.html')
        main = None
        for line in text.split('\n'):
            if self.main_category_match.match(line):
                m = self.main_category_regex.match(line)
                main = Category(m.group(1), m.group(2))
                result.append(main)
            elif main:
                m = self.category_regex.match(line)
                if m:
                    main.addCategory(m.group(1), m.group(2))
        self.categories = result

        print 'Saving categories...'
        for category in self.categories:
            category.save()
        print 'Finished saving'

        self.lock = threading.Semaphore(self.concurrent_threads)
        threads = []
        parsed = set()
        for main_category in self.categories:
            for category in main_category.categories:
                if category.id in parsed:
                    continue
                parsed.add(category.id)
                th = threading.Thread(target=self.parse_category, args=(category,))
                th.start()
                threads.append(th)

        for th in threads:
            th.join()

        self.done = True
        return result

    def parse_category(self, category):
        self.lock.acquire()
        try:
            page, start  = self.read_page(category.id)
            start = int(start) if start else 0
            page = int(page) if page else 1
            print 'starting category %s from %s page %s item' % (category.id, page, start)
            baselink = category.link
            while True:
                if page>1:
                    link = baselink.replace('.html', '/%s.html' % page)
                else:
                    link = baselink
                items = self.getItems(link)
                if not items:
                    print 'no items on the page %s at %s' % (page, link)
                    break
                items = items[start:]

                threads = []
                lock = threading.Semaphore(self.concurrent_products)
                for item in items:
                    th = threading.Thread(target=self.parse_items_thread, args=(lock, category, [item],))
                    th.start()
                    threads.append(th)

                for thread in threads:
                    thread.join()
                    del thread
                    start += 1
                    self.write_page(category.id, page, start)
                del threads
                del lock
                page += 1
                start = 0
                self.write_page(category.id, page, start)
                gc.collect()
                objgraph.show_most_common_types(limit=30)

        except:
            print 'Error while parsing category'
            traceback.print_exc()
            pass
        self.lock.release()
        connection.close()
        print 'Category %s finished' % category.id

    def read_page(self, category_id):
        try:
            f = open('/server/www/Electrosha/media/categories/%s' % category_id)
            page = f.read().split('-')
            f.close()
            return page
        except Exception, e:
            return 1,0

    def write_page(self, category_id, page, index):
        f = open('/server/www/Electrosha/media/categories/%s' % category_id, 'w+')
        f.write('%s-%s' % (page, index))
        f.close()
        del f

    def parse_items_thread(self, lock, category, items):
        lock.acquire()
        try:
            for item in items:
                try:
                    text = get(item.link)
                    if len(text)<50:
                        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> empty link <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<', '\n', 'link=', item.link
                    if self.parse_product(text, item):
                        item.save(category.id)
                        aliexpress.done_count += 1
                        print 'Product saved'
                    del item
                except Exception, e:
                    print 'Product error:', item.link, '\n', e
                    if item.id:
                        error = db_product_failed()
                        error.product_id = item.id
                        error.category_id = category.id
                        error.link = item.link
                        error.error = str(e)
                        error.save()
                    traceback.print_exc(file=sys.stdout)
        except:
            pass
        lock.release()
        connection.close()

    def getItems(self, link):
        """Возвращает список продуктов на странице, указанной в ссылке"""
        result = []
        #print 'get items...'
        text = get(link)
        #print 'got', text[:100]
        for m in self.item_regex.findall(text):
            result.append(Item(m[0], m[1]))
        return result

    def exists(self, id):
        try:
            return db_product.objects.filter(product_id=id).exists()
        except:
            return False

    def parse_product(self, text, item):
        """Парсит информацию об одном продукте"""
        #print 'parse_product'
        #oldtext = text
        start = datetime.datetime.now()
        w = watch()
        item.id = parser.get_value(r'productId="(\d*?)"', text)
        w.measure()

        if self.exists(item.id):
            print 'Exists'
            return False

        link = parser.get_value(r'<a href="([^"]*?)" id="lnk-enlarge-image" target="_blank" title=".*?">.*?<\/a>', text)
        w.measure()
        if link:
            m = get(link)
            link = parser.get_value(r'<div class="image">[\s\S]+?<img src="([^"]*?)".*?>[\s\S]+</div>', m)
            if link:
                item.image = Image(link)
                item.image.download()
        w.measure()

        for link in parser.findall(r'<li\s*?class="image-nav-item"\s*?>.*?<img.*?src="([^"]*?\.jpg).*?\.jpg".*?/>.*?</li>', text):
            image = Image(link)
            try:
                image.download()
                item.gallery.append(image)
            except:
                pass

        item.price = parser.get_value(r'"sku-price".*?>([^<]*?)</span>', text)      
        item.pieces = parser.get_value(r'class="unit-disc"\s*?>\s*?(\d*?)\s', text)
        item.keywords_en = parser.get_value(r'<meta name="keywords" content="([^"]+?)" />', text)
        item.keywords_ru = translator.translate(item.keywords_en)
        item.description_en = parser.get_value(r'<meta name="description" content="([^"]+?)" />', text)
        item.description_ru = translator.translate(item.description_en)
        item.discount = parser.get_value(r'"sku-discount-price".*?>([^<]*?)</span>', text)
        item.discounttime = parser.get_value(r'<span class="time-left">\((\d+?)  days left \)</span>', text)
		
        item.pieces_text_en = ''
        item.pieces_text_ru = ''
        pieces_text = parser.get_value(r'<span class="unit-disc">\s*([^<]+?/[^<]+?\S)\s*,', text)
        if pieces_text:
            item.pieces_text_en = pieces_text
            item.pieces_text_ru = translator.translate(pieces_text)
		
        item.bulk_price_en = parser.get_value(r'<span id="sku-bulk-price">\s*(\S.*?\S)\s*</dd>', text)
        if item.bulk_price_en:
            item.bulk_price_en = item.bulk_price_en.replace('</span>', '');
            item.bulk_price_ru = translator.translate(item.bulk_price_en)
            item.processing_time_en = parser.get_value(r'<dd class="proce-time">\s*(.*?)\s*</td>', text)
            item.processing_time_ru = translator.translate(item.processing_time_en)
        else:
            item.bulk_price_en = ''
            item.bulk_price_ru = ''

        m = parser.get_value(r'<div class="params">(.*?)</div>', text)
        w.measure()
        if m:
            item.specifics = parser.findall(r'<dl>.*?<dt>([^:<]*?):</dt>.*?>([^<]*?)</dd>', m)
            ru = []
            value = []
            for s_en in item.specifics:
                value.append(s_en[0] + ' : ' + s_en[1])
            for s_ru in translator.translate('|'.join(value)).split('|'):
                ru.append(s_ru.split(':'))
            item.specifics_ru = ru
        m = parser.get_value(r'"pdt-pnl-packaging" class="pnl-packaging">(.*?)</div>', text)
        if m:
            item.packaging = parser.findall(r'<dl>.*?<dt>([^:<]*?):</dt>.*?>([^<]*?)</dd>', m)
        w.measure()

        url = r'/cross-domain/freight/index.html?f=d&productid=%s&country=RU&count=1&userType=cgs'
        xml = get(url % item.id)

        freight = ''
        shipping_price = 999999
        tmp = ''
        for one in parser.findall(r'<freight>(.*?)</freight>', xml):
            tmp = parser.get_value(r'<price>(.*?)</price>', one)
            if float(tmp) < float(shipping_price):
                shipping_price = tmp
                freight = one
        if shipping_price == 999999:
            item.shipping = 0
        else:
            item.shipping = shipping_price
        item.shipping_time = parser.get_value(r'<time>(.*?)</time>', freight)

        w.measure()

        text = parser.get_value(r'class="description"(.*?)pdt-pnl-packaging', text)
        if not text:
            print '#############################################################'
            print '#############################################################'
            print '#############################################################'
            print '#############################################################'
            #f = open(r'f:\bad.txt', 'w')
            #f.write(oldtext)
            #f.flush()
            #f.close()
            #return
        try:
            text = re.sub(r'<script[^>]*?>.*?</script>', '', text, flags = re.MULTILINE|re.DOTALL)
        except TypeError,e:
            print '***************************Type Error***********************', '\nType =', text.__class__
        text = re.sub(r'<style[^>]*?>.*?</style>', '', text, flags = re.MULTILINE|re.DOTALL)
        w.measure()
        for link in parser.findall(r'<img.*?src="([^"]*)"', text):
            image = Image(link)
            try:
                image.download()
                item.images.append(image)
            except:
                pass
        w.measure()

        text = re.sub(r'[\s\a\e\f\n\r\t]+', ' ', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'<([a-z0-9]+) .*?>', r'<\1>', text, re.MULTILINE|re.DOTALL)
        text = re.sub('&nbsp;', r'', text, re.MULTILINE|re.DOTALL)
        text = re.sub('<span>', r'', text, re.MULTILINE|re.DOTALL)
        text = re.sub('</span>', r'', text, re.MULTILINE|re.DOTALL)
        text = re.sub('<strong>', r'', text, re.MULTILINE|re.DOTALL)
        text = re.sub('</strong>', r'', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'<img>', r'', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'<img/>', r'', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'>\s+<',     r'><', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'<h2>Product Description</h2>', '', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'<div>', r'<p>', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'</div>', r'</p>', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'"', r"'", text, re.MULTILINE|re.DOTALL)
        w.measure()
        result = []
        for p in parser.findall(r'<p>([\s\S]+)</p>', text):
            p = p.strip()
            if not p:
                continue
            result.append(p)
        w.measure()
        text = '</p><p>'.join(result)
        text = re.sub(r'www.aliexpress.com', u'электроша.рф', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'aliexpress.com', u'электроша.рф', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'aliexpress', u'электроша', text, re.MULTILINE|re.DOTALL)
        text = re.sub(r'', '', text, re.MULTILINE|re.DOTALL)
        w.measure()

        image_html = []
        for image in item.images:
            image_html.append(r"<img src='%s' />" % image.local)
        image_html = ''.join(image_html)
        w.measure()

        item.information_en = text 
        w.measure()
        item.information_ru = translator.translate(text) 
        w.measure()
        item.loaded = True
        delta = (datetime.datetime.now() - start).total_seconds()
        #print 'Product parsed in %s seconds' % delta
        #w.show()
        print 'item parsed'
        return True

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


