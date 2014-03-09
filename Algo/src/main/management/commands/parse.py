from django.core.management.base import BaseCommand, CommandError
import urllib2, hashlib, os, settings, re
from main.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 73):
            try:
                url = 'http://code.activestate.com/recipes/tags/algorithms/top/?page=' + str(i)
                print(url);
                text = self.fetch(url)
                p = re.compile('<span class="recipe-title"><a href="(/recipes/[^/]+/)">[^<]+</a></span>')
                urls = p.findall(text)

                p_title = re.compile('<h1>(.*?)\(.*? recipe\)', re.DOTALL or re.UNICODE)
                p_download = re.compile('<a href="([^"]+/download/\d+/)">', re.UNICODE)
                p_descr = re.compile('<div id="description">(.*?)</div>', re.DOTALL ^ re.UNICODE)
                p_descr2 = re.compile('<div class="proseblock">(.*?)</div>', re.DOTALL ^ re.UNICODE)
                p_lang = re.compile('<div class="block-toolbar as_secondary">\s*<span style="float: right;">([^<]+), \d+ lines</span>')
                p_tags = re.compile('<a href="/recipes/tags/[^"]+/" class="tag">([^<]+)</a>', re.UNICODE)
                p_tags_wrap = re.compile('<ul class="nomachinetags flat">(.*?)</ul>', re.DOTALL or re.UNICODE)
                for url in urls:
                    url = ' http://code.activestate.com' + url
                    print(url)
                    text = self.fetch(url)
                    title = p_title.findall(text)[0].replace('\n', ' ').strip()
                    if not title:
                        print('-')
                        continue
                    download = p_download.findall(text)
                    if len(download) == 0:
                        print('-')
                        continue
                    code = self.fetch('http://code.activestate.com' + download[0])
                    descr = p_descr.findall(text)[0].strip()
                    descr2 = p_descr2.findall(text)
                    if len(descr2):
                        descr2 = descr2[0].strip()
                    else:
                        descr2 = ''

                    lang = p_lang.findall(text)
                    if not len(lang):
                        continue
                    else:
                        lang = lang[0]
                    tags_wrap = p_tags_wrap.findall(text)[0]
                    tags = p_tags.findall(tags_wrap)
                    tags.append(url)

                    Lang = LanguageModel.objects.get(name=lang)
                    if not Lang:
                        print('-')
                        continue
                    Algo = AlgorithmModel()
                    Algo.name = title
                    Algo.description = descr + '<hr />' + descr2
                    Algo.verified = 1
                    Algo.save()

                    Imp = ImplementationModel()
                    Imp.algorithm_id = Algo.id
                    Imp.language_id = Lang.id
                    Imp.source = code
                    Imp.save()

                    for tag in tags:
                        Tag = TagModel.objects.filter(name=tag)
                        if not Tag:
                            Tag = TagModel()
                            Tag.name = tag
                            Tag.save()
                        else:
                            Tag = Tag[0]
                        Algo.tags.add(Tag)

                    Algo.save()
            except Exception, e:
                print e


    def fetch(self, url, cache=True):
        filename = settings.MEDIA_ROOT + '/cache/' + self.md5(url) + '.html'
        if os.path.exists(filename):
            f = open(filename, 'r')
            text = f.read()
            f.close()
            return text
        text = urllib2.urlopen(url).read()
        f = open(filename, 'w+', 0777)
        f.write(text)
        f.close()
        return text

    def md5(self, value):
        m = hashlib.md5()
        m.update(value)
        return m.hexdigest()