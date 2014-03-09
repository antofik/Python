def insertion_sort(iterable):
    for i in xrange(len(iterable)):
        item = iterable.pop(i)
        for j in xrange(i - 1, -1, -1):
            if item >= iterable[j]:
                iterable.insert(j + 1, item)
                break
        else:
            iterable.insert(0, item)


def bubble_sort(iterable):
    for i in xrange(len(iterable)):
        for j in xrange(len(iterable) - 1):
            if iterable[j + 1] > iterable[j]:
                iterable[j + 1], iterable[j] = iterable[j], iterable[j + 1]


from random import shuffle
from time import clock as now

N = 10000
r = range(N)
shuffle(r)
start = now()
insertion_sort(r)
#bubble_sort(r)
print 'Sorted %s items in %sms' % (N, round(now() - start, 3))

print r[:20]