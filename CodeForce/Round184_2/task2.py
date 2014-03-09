# coding=utf-8
"""
task_description
"""
from sys import stdin, exit


def task():
    p, q = map(int, stdin.readline().split())
    n = int(stdin.readline())
    a_n = map(int, stdin.readline().split())
    for i, a in enumerate(a_n, 1):
        r, p = divmod(p, q)
        if i < n and p == 0:
            r -= 1
            p = q
        if r != a:
            print 'NO'
            quit()
        p, q = q, p
    print 'YES' if q == 0 else 'NO'


task()
