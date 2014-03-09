import random

n = 1000
f = open('test1_4', 'w+')

f.write('%s\n' % n)
t = 0
for i in range(n):
        t += random.randrange(1,10)
        f.write(('%s %s\n' % (t, random.randrange(0,100000000000))))
f.close()