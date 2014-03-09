# coding=utf-8
"""
task_description
"""
from sys import stdin, exit

print 'This is task 5'
n, m = map(int, stdin.readline().split())
values = [(int(x), int(y)) for x, y in map(str.split, stdin.readlines())]
