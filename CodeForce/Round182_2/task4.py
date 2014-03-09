# coding=utf-8
"""
D. Ярослав и время
ограничение по времени на тест:2 секунды
ограничение по памяти на тест:256 мегабайт
ввод:standard input
вывод:standard output

Ярослав играет в игру «Время». В игре у него есть таймер, на котором изображено время, которое ему осталось жить. Как только таймер показывает 0, игровой персонаж Ярослава умирает и игра заканчивается. Так же в игре существует n часовых станций, станция номер i находится в точке (xi, yi) плоскости. Зайдя на станцию номер i, игрок увеличивает текущее время на своем таймере на ai. Станции одноразовые, то есть если игрок второй раз зайдет на какую-нибудь станцию, то время на его таймере не увеличится.

На перемещение между станциями игрок тратит d·dist единиц времени, где dist — расстояние, пройденное игроком, а d — некоторая константа. Расстояние между станциями i и j определяется как |xi - xj| + |yi - yj|.

Изначально игрок находится на станции номер 1, и у игрока осталось строго больше нуля и меньше одной единицы времени. На станции номер 1 за единицу денег можно увеличить время на таймере на единицу времени (можно покупать только целое количество единиц времени).

Сейчас Ярослава интересует вопрос: сколько единиц денег нужно ему, чтобы попасть на станцию номер n? Помогите Ярославу. Считайте, что время покупки и увеличения времени на таймере пренебрежимо мало.
Входные данные

В первой строке содержатся целые числа n и d (3 ≤ n ≤ 100, 103 ≤ d ≤ 105) — количество станций и константа из условия.

Во второй строке заданы n - 2 целых числа: a2, a3, ..., an - 1 (1 ≤ ai ≤ 103). В следующих n строках содержатся координаты станций. В i-той из них записаны два целых чисел xi, yi (-100 ≤ xi, yi ≤ 100).

Гарантируется, что никакие две станции не находятся в одной точке.
Выходные данные

В единственную строку выведите целое число — ответ на задачу.
"""
from sys import stdin, exit


def task():
    n, d = map(int, stdin.readline().split())
    a = map(int, stdin.readline().split())
    stations = [(int(x), int(y)) for x, y in map(str.split, stdin.readlines())]

    start = stations[0]
    end = stations[-1]
    stations = zip(stations[1:-1], a)

    distance = lambda l1, l2: abs(l1[1] - l2[1]) + abs(l1[0] - l2[0])
    cost = distance(start, end)
    print cost

    rect = min(start[0], end[0]), min(start[1], end[1]), max(start[0], end[0]), max(start[1], end[1])

    def is_inside(x, y):
        if x < rect[0] or x > rect[2]:
            return False
        if y < rect[1] or y > rect[2]:
            return False
        return True

    def get_rect_cost():
        inside_cost = sum([a for l, a in stations if is_inside(s[0])])
        cost = abs(rect[2] - rect[0]) + abs(rect[3] - rect[0])
        return inside_cost - cost

    max_cost = get_rect_cost()


    def station_cost(x, y, station, income):
        return income


    def is_good(station):
        (x, y), a = station
        if is_inside(x, y):
            return False
        delta = 0
        if x < rect[0]:
            delta += 2 * abs(x - rect[0])
        elif x > rect[2]:
            delta += 2 * abs(x - rect[2])
        if y < rect[1]:
            delta += 2 * abs(y - rect[1])
        elif y > rect[3]:
            delta += 2 * abs(y - rect[3])
        if max_cost >= a - delta * d >= 0:
            return True

    while True:
        inside_stations = [s for s in stations if is_inside(s[0])]



task()
