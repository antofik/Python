# coding=utf-8
"""
D. Покраска квадрата
ограничение по времени на тест3 секунды
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
У медведя Василия есть большая квадратная таблица белого цвета, составленная из n строк и n столбцов. Вокруг этой таблицы очерчена граница черной краской.

Пример изначальной таблицы при n = 5.
Медведь Василий хочет ровно за k ходов покрасить свою квадратную таблицу. Каждый ход — это последовательность действий:

Медведь выбирает некоторый квадрат внутри своей таблицы, причем вокруг квадрата должна должна быть очерчена граница черной краской, а также внутри квадрата не должно быть ячейки, закрашенной в черный цвет. Количество ячеек в квадрате должно быть не меньше 2.
Медведь выбирает внутри выбранного квадрата некоторую строку и некоторый столбец. Далее он закрашивает каждую ячейку этой строки и этого столбца внутри выбранного квадрата. После описанной операции прямоугольники, образованные границей квадрата и только что закрашенными ячейками, должны являться квадратами ненулевой площади.

Пример корректной покраски при n = 7 и k = 2.
Медведь уже знает числа n и k. Помогите ему — найдите количество способов покрасить его квадрат ровно за k действий. Два способа покраски называются различными, если полученные таблицы будут различаться цветом хотя бы в одной ячейке. Так как ответ может быть большим, выведите его остаток от деления на 7340033.

Входные данные
В первой строке записано целое число q (1 ≤ q ≤ 105) — количество тестовых данных.

В каждой из следующих q строк содержатся два целых числа n и k (1 ≤ n ≤ 109, 0 ≤ k ≤ 1000) — размер изначальной таблицы и количество ходов для соответствующего теста.

Выходные данные
Для каждого теста из входных данных выведите ответ на задачу по модулю 7340033. Ответы для тестов выводите в том порядке, в котором тесты заданы во входных данных.
"""
from sys import stdin

mod = 7340033


def depth(n):
    d = 0
    while n > 1 and n % 2 == 1:
        d += 1
        n /= 2
    return d


def max_k(d):
    if d == 0:
        return 0
    return (pow(4, d-1) - 1)/3


def calc(max_d, max_k):
    c = [[0]*(max_k + 1) for _ in xrange(max_d + 1)]
    c[0][0] = 1
    for d in xrange(1, max_d + 1):
        c[d][0] = 1

        t = [0] * (max_k * 2 + 2)
        for k1 in xrange(max_k):
            for k2 in xrange(max_k):
                t[k1 + k2] += c[d-1][k1]*c[d-1][k2]
        for i in xrange(max_k*2+2):
            t[i] %= mod
        for k1 in xrange(max_k):
            for k2 in xrange(max_k - k1):
                c[d][k1 + k2 + 1] += t[k1]*t[k2]
        for i in xrange(max_k+1):
            c[d][i] %= mod
    return c


def main():
    stdin.readline()
    q = [map(int, line.split()) for line in stdin.readlines()]
    q = [(n, depth(n), k) for n, k in q]

    max_d = max(q, key=lambda q: q[1])[1]
    max_k = max(q, key=lambda q: q[2])[2]

    c = calc(max_d, max_k)

    for n, d, k in q:
        print c[d][k]

main()