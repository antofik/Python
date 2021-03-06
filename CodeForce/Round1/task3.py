# coding=utf-8
"""
C. Древнеберляндский цирк
ограничение по времени на тест:2 seconds
ограничение по памяти на тест:64 megabytes
ввод:standard input
вывод:standard output

Это сейчас все цирки в Берляндии имеют круглую арену диаметром 13 метров, а в древности все было совсем иначе.

В Древней Берляндии цирки имели арены в форме правильных многоугольников, а размеры и количества углов могли варьироваться от цирка к цирку. В каждом углу арены в землю был заколочен специальный столб, а на них были натянуты канаты, ограничивающие арену.

Недавно ученые Берляндии раскопали останки арены древнего цирка. Ими было найдено всего три столба, остальные были уничтожены временем.

Ваша задача по координатам найденных трех столбов определить, какую наименьшую площадь могла иметь арена этого цирка.
Входные данные

Входной файл состоит из трех строк, каждая из которых содержит пару чисел — координаты столба. Любая из координат не превосходит по абсолютной величине 1000, и задана с 6 знаками после десятичной точки.
Выходные данные

Выведите искомую площадь с точностью не менее 6 знаков после точки. Гарантируется, в оптимальном многоугольнике будет не более 100 вершин.
Примеры тестов
Входные данные
0.000000 0.000000
1.000000 1.000000
0.000000 1.000000
Выходные данные
1.00000000
"""

from sys import stdin
import math

v1, v2, v3 = [(float(a), float(b)) for a,b in map(str.split, stdin.readlines())]
(x1, y1), (x2, y2), (x3, y3) = v1, v2, v3


def get_circle_center(v1, v2, v3):
    (x1, y1), (x2, y2), (x3, y3) = v1, v2, v3
    if x1 == x2:
        return (x1 + x3 - (y3 - y1)*(y3 - y2)/(x1 - x3))/2, (y1 + y2)/2
    elif x1 == x3:
        return (x1 + x2 - (y2 - y1)*(y2 - y3)/(x1 - x2))/2, (y1 + y3)/2
    m2 = (y2 - y1)/(x1 - x2)
    m3 = (y3 - y1)/(x1 - x3)
    y0 = (0.5/(m3 - m2)) * (-m2*(y1 + y2) + m3*(y1 + y3) + x2 - x3)
    x0 = 0.5 * (x1 + x2 - m2 * (y1 + y2 - 2*y0))
    return x0, y0


def len(x, y):
    return math.sqrt(x*x + y*y)

def angle(x1, y1, x2, y2):
    l1 = len(x1, y1)
    l2 = len(x2, y2)
    p = x1*x2 + y1*y2
    v = p/(l1*l2)
    if v < -1:
        v = -1
    if v > 1:
        v = 1
    return math.acos(v)

def find_real_number(a1, a2, a3):
    for n in range(1,101):
        d = 0
        b1 = b2 = b3 = 0
        for m in range(1,n):
            angle = 2*math.pi*m/n
            if abs(angle - a1) <= 0.000001:
                b1 = m
            if abs(angle - a2) <= 0.000001:
                b2 = m
            if abs(angle - a3) <= 0.000001:
                b3 = m
                break
        if b3 >= b2 >= b1 > 0:
            break
    return n


x0, y0 = v0 = get_circle_center(v1, v2, v3)
x1 -= x0
x2 -= x0
x3 -= x0
y1 -= y0
y2 -= y0
y3 -= y0
l1 = len(x1, y1)
l2 = len(x2, y2)
l3 = len(x3, y3)

a1 = angle(x1, y1, x2, y2)
a2 = angle(x1, y1, x3, y3)
a3 = angle(x2, y2, x3, y3)
l = len(x1, y1)
n = find_real_number(*sorted([a1, a2, a3]))
s = (n/2.0)*l*l*math.sin(2*math.pi/n)

print '%f' % s