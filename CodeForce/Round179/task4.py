from sys import stdin
try:
    from dev import stdin
except ImportError:
    pass


n, m = [int(i) for i in stdin.readline().split()]
up = {}
down = {}

result = 0
f = False
even = False
threshold = n // 2 - 1
half_row = (n - 1) / 2.0
m_1 = m - 1

prev = [0] * m
for row in xrange(0, n):
    u = 0
    s = 0
    if not f:
        f = row > threshold
    even = row == half_row
    _row = n - row - 1
    for l in xrange(1, m):
        p = prev[l]
        d = u + s
        s += p
        u = (d + p) % 1000000007
        _u = u + 1
        prev[l] = _u
        if not f:
            k = (row, l)
            up[k] = _u
            down[k] = (d + 1)
        else:
            if not even:
                result += (_u * down[(_row, l)] + (d + 1) * up[(_row, l)]) * (m - l) % 1000000007
            else:
                result += (d + 1) * _u * (m - l)

print int(result % 1000000007)
#631601096