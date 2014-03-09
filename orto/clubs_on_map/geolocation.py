import httplib
import re
from time import sleep

request_pattern = "/1.x/?geocode=%s&format=json&results=1&lang=ru-RU"

regex = re.compile(r'pos":"(.*?)"', re.MULTILINE | re.UNICODE)
output = open('results.sql', 'w+')

for line in open('clubs.csv').read().split('\n'):
    clubid, address, city, country = line.split(';')
    fulladdress = '%s, %s, %s' % (country, city, address)
    connection = httplib.HTTPConnection("geocode-maps.yandex.ru")
    connection.request('GET', request_pattern % fulladdress)
    while True:
        response = connection.getresponse()
        if response.status == 200:
            break
        sleep(10)

    data = response.read()
    search = regex.search(data)
    if search:
        try:
            longitude, latitude = map(float, search.group(1).split())
            print '%s => %s, %s, %s' % (clubid, longitude, latitude, address)
            output.write('update club set lon=%s, lat=%s where id=%s;' % (longitude, latitude, clubid))
        except Exception, e:
            print str(e)

    sleep(1)

output.close()
quit()