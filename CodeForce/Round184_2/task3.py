# coding=utf-8
"""
task_description
"""
from sys import stdin


def task():
    stdin.readline()
    a = map(int, stdin.readline().split())
    a.reverse()
    result = 0
    i = 0
    reminder = 0
    while a or reminder:
        while a and a[-1] == i:
            reminder += 1
            a.pop()
        result += reminder % 2 == 0
        reminder /= 2
        if reminder > 0:
            i += 1
        elif a:
            result += a[-1] - i - 1
            i = a[-1]
    print result


task()