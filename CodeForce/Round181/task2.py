# coding=utf-8
"""
task_description
"""
from sys import stdin, exit

n, m = map(int, stdin.readline().split())
lines = [(int(a), int(b)) for a, b in map(str.split, stdin.readlines())]
pairs = {}
#print 'Input=%s' % lines
p = set(lines)

for a, b in lines:
    if a in pairs:
        s = pairs[a]
        if b in pairs and b not in s:
            print -1
            exit()
        s.add(b)
        for i in s:
            pairs[i] = s
        if len(s) > 3:
            print -1
            exit()
    elif b in pairs:
        s = pairs[b]
        if a in pairs and a not in s:
            print -1
            exit()
        s.add(a)
        for i in s:
            pairs[i] = s
        if len(s) > 3:
            print -1
            exit()
    else:
        s = {a, b}
        for i in s:
            pairs[i] = s

#print 'Pairs=%s' % pairs

triples = []
twos = []

singles = []
for i in xrange(1, n + 1):
    if i in pairs:
        s = pairs[i]
        if len(s) == 3:
            if not s in triples:
                triples.append(s)
        else:
            if not s in twos:
                twos.append(s)
    else:
        singles.append(i)

if len(twos) > len(singles):
    print -1
    exit()

#print '>>>', twos
#print '>>>', singles
#print '>>>', triples

while twos:
    p = twos.pop()
    s = singles.pop()
    p.add(s)
    triples.append(p)


while singles:
    s = {singles.pop(), singles.pop(), singles.pop()}
    triples.append(s)

#print 'n=%s' % n
#print 'Singles=%s' % singles
#print 'Twos=%s' % twos
#print 'Triples=%s' % triples

for triple in triples:
    print ' '.join(map(str,triple))

