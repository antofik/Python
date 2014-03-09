# coding=utf-8
"""
task_description
"""
from sys import stdin


def task():
    n, m = map(int, stdin.readline().split())
    a = map(int, stdin.readline().split())
    b = map(int, stdin.readline().split())
    a.sort()
    b.sort()
    a.reverse()

    result = []
    j = 0
    bi = b[0]
    for ai in a:
        j += 1
        bi = b[j]



task()
