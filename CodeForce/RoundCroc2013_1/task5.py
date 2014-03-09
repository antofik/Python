# coding=utf-8
"""
E. Древесно-строковая задача
ограничение по времени на тест:2 секунды
ограничение по памяти на тест:256 мегабайт
ввод:standard input
вывод:standard output

Корневым деревом называется неориентированный связный граф без циклов с выделенной вершиной, которая называется корнем
дерева. Будем считать, что вершины корневого дерева из n вершин пронумерованы от 1 до n. В этой задаче корнем дерева
будет вершина с номером 1.

Обозначим через d(v, u) длину кратчайшего по количеству ребер пути в дереве между вершинами v и u.

Родителем вершины v в корневом дереве с корнем в вершине r (v ≠ r) называется вершина pv, такая, что d(r, pv) + 1 = d(r, v)
и d(pv, v) = 1. Например, на рисунке родителем вершины v = 5 является вершина p5 = 2.

Как-то раз Поликарп раздобыл корневое дерево из n вершин. Дерево было не совсем обычное — на его ребрах были написаны
строки. Поликарп расположил дерево на плоскости так, что все ребра ведут сверху вниз при прохождении от родителя
вершины к вершине (см. рисунок). Для каждого ребра, ведущего из вершины pv в вершину v (1 < v ≤ n), известна строка sv,
которая на нем написана. Все строки записаны на ребрах сверху вниз. Например, на рисунке s7=«ba». Символы в строках
пронумерованы от 0.
"""
from collections import defaultdict
from sys import stdin


def compute_prefix_function(p):
    m = len(p)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and p[k] != p[q]:
            k = pi[k - 1]
        if p[k] == p[q]:
            k += 1
        pi[q] = k
    s = set(p)
    l = defaultdict(int)
    l.update({c: 0 for c in s})
    r = [l]
    r[0][p[0]] = 1
    for i, ch in enumerate(p[1:], start=1):
        l = defaultdict(int)
        l.update({c: [r[pi[i-1]][c], i + 1][ch == c] for c in s})
        r.append(l)
    l = defaultdict(int)
    l.update({c: r[pi[-1]][c] for c in s})
    r.append(l)
    return r


def task():
    n = int(stdin.readline())
    counter = 0
    tree = defaultdict(list)
    words = []
    pattern = ''

    for index, value in enumerate(stdin.readlines()):
        if index < n - 1:
            parent_string, word = value.split()
            words.append(word)
            tree[int(parent_string) - 2].append(index)
        elif index == n - 1:
            pattern = value.strip()

    length = len(pattern)
    search = [(0, child) for child in tree[-1]]

    pi = compute_prefix_function(pattern)

    append, pop = search.append, search.pop
    while search:
        matchLen, index = pop()
        for c in words[index]:
            matchLen = pi[matchLen][c]
            if matchLen == length:
                counter += 1
        for child in tree[index]:
            append((matchLen, child))

    print counter


task()
