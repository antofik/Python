# coding=utf-8
"""
B. Евгений и плейлист
ограничение по времени на тест:2 секунды
ограничение по памяти на тест:256 мегабайт
ввод:standard input
вывод:standard output

Евгений любит слушать музыку. В плейлисте Евгения играет n песен. Известно, что песня номер i имеет продолжительность ti минут. Каждую песню плейлиста Евгений слушает, возможно, более одного раза. Песню номер i он слушает ci раз. Плейлист Евгения построен следующим образом: сначала c1 раз играет песня номер 1, потом c2 раз играет песня номер 2, ..., в конце cn раз играет песня номер n.

Евгений выписал себе на листочек m моментов времени, в которые ему понравились песни. Теперь для каждого такого момента, он хочет узнать номер песни, которая играла в этот момент времени. Момент времени x обозначает, что Евгений хочет знать, какая песня играла в x-ую от начала минуту прослушивания плейлиста.

Помогите Евгению, выведите требуемые номера песен.
Входные данные

В первой строке заданы два целых числа n, m (1 ≤ n, m ≤ 105). В следующих n строках заданы пары целых чисел. В i-ой строке записаны целые числа ci, ti (1 ≤ ci, ti ≤ 109) — описание плейлиста. Гарантируется, что суммарная продолжительность плейлиста не более 109 .

В следующей строке записаны m целых положительных чисел v1, v2, ..., vm, которые описывают времена, выписанные Евгением. Гарантируется, что не существует момента времени vi, когда музыка уже не играла. Гарантируется, что vi < vi + 1 (i < m).

Момент времени vi обозначает, что Евгений хочет знать, какая песня играла в vi-ую от начала минуту прослушивания плейлиста.
Выходные данные

Выведите m целых чисел — i-ое число должно быть равно номеру песни, которая играла в vi минуту от начала прослушивания плейлиста.
"""
from bisect import bisect_left
from sys import stdin, exit


def task():
    n, m = map(int, stdin.readline().split())
    playlist = {}
    durations = []
    s = 0
    for i in xrange(n):
        c, t = map(int, stdin.readline().split())
        s += c * t
        durations.append(s)
        playlist[s] = i
    requests = map(int, stdin.readline().split())
    result = []
    for r in requests:
        k = bisect_left(durations, r)
        result.append(str(playlist[durations[k]] + 1))
    print '\n'.join(result)


task()
