__author__ = 'anton'

import glob
import os

for filename in glob.glob('views/*.ui'):
    name = filename[6:-3]
    os.system('pyside-uic -o views/ui_%s.py views/%s.ui' % (name, name))
