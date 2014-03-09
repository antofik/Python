# coding=utf-8
"""
task_description
"""
from sys import stdin


def task():
    n, m = map(int, stdin.readline().split())
    values = [(int(x), int(y)) for x, y in map(str.split, stdin.readlines())]
    print 'This is task 5'


task()
