import os
import httplib
import urllib
from optparse import OptionParser

host = 'russianmaster.ru'
url = '/html/registration/DirAndGetFile.php'
www = '/home/kondr/www/russianmaster.ru'

def main():
    (options, args) = parse_options()
    if args:
        for path in args:
            path = convert_path(path)
            download_path(path, options.show_result)
    else:
        print 'Usage: loader.py path1 path2 path3 ...'

def parse_options():
    parser = OptionParser()
    parser.add_option("-s", "--show", action="store_true", dest="show_result")
    return parser.parse_args()

def convert_path(path):
    if not path.startswith('/'):
        path = os.path.join(www, path).replace('\\','/')
    return path

def download_path(path, show_result):
    data = load_path(path)
    if len(data)>3:
        print 'Received: %s bytes' % len(data)
        path = create_path(path)
        save_to_file(path, data)
        print 'Saved to file'
        if show_result:
            print '----------------------------------------------------------------------------'
            print data
    else:
        print 'Failed %s' % data


def load_path(path):
    connection = httplib.HTTPConnection(host)
    params = urllib.urlencode({'evalJSfile': path})
    headers = {"Content-type": "application/x-www-form-urlencoded", 'Accept-Encoding':'deflate'}
    print '=>', path
    connection.request('POST', url, params, headers)
    print headers
    print params
    print url
    response = connection.getresponse()
    data = response.read()
    print response.msg
    return data

def create_path(path):
    root = os.path.abspath(os.path.join(os.curdir, 'data'))
    dirs = path.replace('\\','/').split('/')
    filename = dirs[-1]
    for dir in dirs[:-1]:
        if dir is None: continue
        root = '%s\\%s' % (root, dir)
        if not os.path.exists(root):
            os.mkdir(root)
    return os.path.join(root, filename)

def save_to_file(path, data):
    f = open(path, 'wb')
    f.write(data)
    f.flush()
    f.close()

if __name__=='__main__':
    main()