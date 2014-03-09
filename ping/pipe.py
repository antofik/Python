import os


p = os.popen('test')
while True:
    print p.readline()