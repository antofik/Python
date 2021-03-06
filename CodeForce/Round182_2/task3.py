# coding=utf-8
"""
task_description
"""
from sys import stdin, exit

def task():
    n = int(stdin.readline())
    values = map(int, stdin.readline().split())
    positives = sorted([abs(i) for i in values])
    zero_count = len([i for i in values if i == 0])
    negative_count = len([i for i in values if i < 0])

    if zero_count > 0:
        print sum(positives)
        exit()

    if n % 2 == 0 and negative_count % 2 == 1:
        negative_count = 1
    else:
        negative_count = 0
    negatives = positives[:negative_count]
    positives = positives[negative_count:]
    print sum(positives) - sum(negatives)


task()
