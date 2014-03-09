# coding=utf-8
"""
B. Грузовик
ограничение по времени на тест:2 seconds
ограничение по памяти на тест:64 megabytes
ввод:standard input
вывод:standard output

Группа туристов собирается в водный поход. На лодочную базу прибыл арендованный грузовик, в который будут погружены байдарки и катамараны, а затем доставлены на место отправления. Известно, что все байдарки равны по размерам между собой (и занимают 1 куб. метр пространства), а катамараны равны по размерам между собой и в два раза больше байдарки (и занимают 2 куб. метра пространства).

Каждое плавсредство обладает некоторой грузоподъемностью, причем даже неотличимые с виду плавсредства могут обладать разной грузоподъемностью.

По заданному объему кузова грузовика и списку плавсредств (для каждого известен его тип и грузоподъемность) определите набор, который можно перевести и который обладает максимальной возможной грузоподъемностью. Объем кузова грузовика можно использовать максимально эффективно, то есть в кузов всегда можно погрузить плавсредство объемом не превышающее свободный объем кузова.
Входные данные

В первой строке записана пара целых чисел n и v (1 ≤ n ≤ 105; 1 ≤ v ≤ 109), где n это количество плавсредств на лодочной базе, а v — объем кузова грузовика в кубических метрах. Следующие n строк содержат описания плавсредств. Каждое описание это пара чисел ti, pi (1 ≤ ti ≤ 2; 1 ≤ pi ≤ 104), где ti это тип плавсредства (1 — байдарка, 2 — катамаран), а pi его грузоподъемность. Плавсредства нумеруются с единицы в порядке их появления во входном файле.
Выходные данные

В первую строку выведите искомую максимальную грузоподъемность набора. Во вторую строку выведите номера плавсредств, которые составляют оптимальный набор. Если решений несколько, выведите любое.
"""
from sys import stdin


n, v = map(int, stdin.readline().split())


class boat(object):
    def __init__(self, number, kind, size):
        self.numher = number
        self.kind = kind
        self.size = size
        self.weight = size / kind

    def __str__(self):
        return '#%s: %s %s => %s' % (self.numher, self.kind, int(self.size), self.weight)


boats = [boat(i, int(x), float(y)) for i, (x, y) in enumerate(map(str.split, stdin.readlines()), start=1)]
boats.sort(key=lambda x: x.weight)

selected = []
space = v
sum_size = 0
while space > 1 and boats:
    boat = boats.pop()
    selected.append(boat)
    space -= boat.kind
    sum_size += boat.size

first = None
kandidate = None
while space == 1 and boats:
    boat = boats.pop()
    if not first:
        first = boat
    if boat.kind == 1:
        kandidate = boat
        break

if space == 1:
    if selected:
        for i in range(len(selected) - 1, -1, -1):
            boat = selected[i]
            if boat.kind == 1:
                delta = first.size - boat.size
                if kandidate and kandidate.size > delta:
                    selected.append(kandidate)
                    sum_size += kandidate.size
                    space -= 1
                elif delta > 0:
                    selected.remove(boat)
                    selected.append(first)
                    space -= 1
                    sum_size -= boat.size
                    sum_size += first.size
                break
    elif kandidate:
        selected.append(kandidate)
        sum_size += kandidate.size
        space -= 1

print int(sum_size)
print ' '.join([str(s.numher) for s in selected])
