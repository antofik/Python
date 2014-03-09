# coding=utf-8
"""
D. Компоненты связности
ограничение по времени на тест:2 секунды
ограничение по памяти на тест:256 мегабайт
ввод:standard input
вывод:standard output

В уже известной нам некоторой большой корпорации, в которой работает системный администратор Поликарп, компьютерная сеть
состоит n компьютеров и m кабелей, которые соединяют некоторые пары компьютеров. Другими словами, компьютерная сеть
может быть представлена некоторым неориентированным графом из n вершин и m ребер. Пронумеруем компьютеры целыми числами
от 1 до n, пронумеруем кабели целыми числами от 1 до m.

Поликарпу поручили ответственное задание — проверить надежность компьютерной сети его корпорации. Для этого Поликарп
решил провести серию из k экспериментов с компьютерной сетью, где i-ый эксперимент заключается в следующем:

 Временно отсоединить кабели с номерами от li до ri, включительно (остальные кабели остаются подсоединенными).
 Посчитать количество компонент связности в графе, который определяет компьютерную сеть в настоящий момент.
 Подсоединить отключенные кабели с номерами от li до ri (то есть восстановить исходную сеть).


Помогите Поликарпу провести все эксперименты и для каждого из них выведите количество компонент связности в графе,
который определяет компьютерную сеть во время данного эксперимента. Изолированную вершину нужно считать отдельной
компонентой.

Входные данные

В первой строке через пробел заданы два целых числа n, m (2 ≤ n ≤ 500; 1 ≤ m ≤ 104) — количество компьютеров и количество
кабелей соответственно.

Далее в m строках задано описание кабелей. В i-ой строке через пробел задана пара целых чисел xi, yi
(1 ≤ xi, yi ≤ n; xi ≠ yi) — номера компьютеров, которые соединяет i-ый кабель. Обратите внимание, что пара компьютеров
может быть соединена несколькими кабелями.

В следующей строке задано единственное целое число k (1 ≤ k ≤ 2·104) — количество экспериментов. Далее в k строках
задано описание экспериментов. В i-ой строке через пробелы заданы числа li, ri (1 ≤ li ≤ ri ≤ m) — номера кабелей, которые
Поликарп отсоединяет во время i-го эксперимента.
Выходные данные

Выведите k чисел, в которых i-ое число обозначает количество компонент связности графа, который определяет компьютерную
сеть во время i-го эксперимента.
"""
from sys import stdin


#@profile
def task():
    n, m = map(int, stdin.readline().split())
    readings = stdin.readlines()
    all_cables = [tuple(sorted((int(x) - 1, int(y) - 1), reverse=True)) for x, y in map(str.split, readings[:m])]
    k = int(readings[m])
    experiments = [(int(x) - 1, int(y) - 1) for x, y in map(str.split, readings[m + 1:])]

    left = [[i for i in xrange(n)]]
    right = [[i for i in xrange(n)]]

    def merge(row, x, y):
        t = x
        while row[t] != t:
            t = row[t]
        while row[x] != x:
            x, row[x] = row[x], t

        t = y
        while row[t] != t:
            t = row[t]
        while row[y] != y:
            y, row[y] = row[y], t

        if x != y:
            row[x] = y

    def compress(row):
        stack = range(n)
        while stack:
            x = stack.pop()
            s = [x]
            while row[x] != x:
                x = row[x]
                s.append(x)
                if x in stack:
                    stack.remove(x)
            m = min(s)
            for x in s:
                row[x] = m

    for i in xrange(m):
        row = list(left[i])
        x, y = all_cables[i]
        merge(row, x, y)
        compress(row)
        left.append(row)

    for i in xrange(m):
        row = list(right[i])
        x, y = all_cables[m - 1 - i]
        merge(row, x, y)
        compress(row)
        right.append(row)

    result = []
    for l, r in experiments:
        row = list(left[l])
        row2 = right[m - r - 1]
        for y, x in enumerate(row2):
            while row[x] != x or row[y] != y:
                x, y = row[x], row[y]
            row[y] = x
        result.append(sum([x == y for x, y in enumerate(row)]))

    #print '\n'.join(map(str, result))

task()