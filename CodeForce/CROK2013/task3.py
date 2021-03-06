import sys, itertools
sys.setrecursionlimit(10001)

def valid(num):
    n = int(num)
    if str(n) != num:
        return False
    return 0 <= n <= 255


def div_ip1(n):
    for x in xrange(2, len(n)-1):
        for ip1 in div_ip2(n[:x]):
            for ip2 in div_ip2(n[x:]):
                yield ip1 + "." + ip2

def div_ip2(n):
    for x in xrange(1, len(n)):
        if valid(n[:x]) and valid(n[x:]):
            yield n[:x] + "." + n[x:]

def to_ip(n):
    s = ""
    for i in n:
        s += str(i)
    return s

def merge(num):
    m.add(to_ip(num))
    if len(num) < 6:
        for a in A:
            for i in xrange(len(num) + 1):
                num.insert(i, a)
                m.add(to_ip(num))
                merge(num)
                num.pop(i)

sys.stdin = open('test3_1')
n = int(sys.stdin.readline().strip())
A = map(int, sys.stdin.readline().strip().split())

ans = set()
if n <= 6:
    for ls in itertools.permutations(A, n):
        m = set()
        merge(list(ls))
        for p in m:
            for x in div_ip1(p + p[::-1]):
                ans.add(x)
            for x in div_ip1(p + p[-2::-1]):
                ans.add(x)
print len(ans)
#for ip in ans:
#    print ip