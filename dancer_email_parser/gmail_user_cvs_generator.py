# coding=utf-8
from io import open

__author__ = 'anton'

with open('gmail.csv', 'w') as f:
    f.write(u"email address,first name,last name,password\n")
    for i in xrange(5,100):
        f.write(u"noreply%s,noreply,noreply,noreply$$$\n" % i)