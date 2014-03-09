# coding=utf-8
"""
D. Загадочная посылка
ограничение по времени на тест:2 seconds
ограничение по памяти на тест:64 megabytes
ввод:standard input
вывод:standard output

Петя решил поздравить своего друга из Австралии с предстоящим днем рождения, отправив ему открытку. Чтобы сделать свой сюрприз более загадочным, он решил создать цепь. Цепью назовем такую последовательность конвертов A = {a1, a2, ..., an}, что ширина и высота i-го конверта строго больше ширины и высоты (i - 1)-го соответственно, а размером цепи — количество конвертов в ней. Из имеющихся у Пети конвертов он хочет создать наибольшую по размеру цепь, в которую можно было бы вложить открытку. Открытку можно вложить в цепь, если ширина и высота открытки меньше ширины и высоты меньшего конверта в цепи соответственно. Поворачивать конверты или открытку запрещено. Поскольку у Пети очень много конвертов и очень мало времени, то эта нелегкая задача возлагается на Вас.
Входные данные

Первая строка содержит целые числа n, w, h (1 ≤ n ≤ 5000, 1 ≤ w, h ≤ 106) — количество конвертов, имеющихся у Пети в распоряжении, ширину и высоту открытки соответственно. Далее содержится n строк, в каждой из которых находится два целых числа wi и hi — ширина и высота i-го конверта (1 ≤ wi, hi ≤ 106).
Выходные данные

В первую строку выведите размер максимальной цепи. Во вторую строку выведите через пробелы номера конвертов, образующих такую цепь, начиная с номера наименьшего конверта. Помните, что в наименьший конверт должна поместиться открытка. Если существует несколько цепей максимального размера, выведите любую.

Если открытка не помещается ни в один конверт, то выведите единственную строку, содержащую число 0.
"""
from bisect import bisect_left
from sys import stdin, exit
from operator import itemgetter

def task():
    n, w, h = map(int, stdin.readline().split())
    i = 1
    letter = []
    for x, y in [(int(x), int(y)) for x, y in map(str.split, stdin.readlines())]:
        if x > w and y > h:
            letter.append((x, y, i))
        i += 1

    n = len(letter)
    letter.sort(key=itemgetter(1), reverse=True)
    letter.sort(key=itemgetter(0))

    dp = []
    d = [0] * n
    for i, key in enumerate(letter):
        k = bisect_left(dp, key[1])
        d[i] = k
        if k < len(dp):
            dp[k] = key[1]
        else:
            dp.append(key[1])

    print len(dp)

    r = []
    l = len(dp)
    for i in xrange(n - 1, -1, -1):
        if d[i] == l - 1:
            r.append(letter[i][2])
            l -= 1
            if l < 0:
                break
    r.reverse()
    if r:
        print ' '.join(map(str, r))


task()