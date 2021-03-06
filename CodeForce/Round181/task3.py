# coding=utf-8
"""
C. Прекрасные числа
ограничение по времени на тест2 секунды
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
Виталий очень странный человек. У него есть две любимые цифры a и b. Виталий называет целое положительное число хорошим, если в десятичной записи этого числа используются только цифры a и b. Виталий называет хорошее число замечательным, если сумма его цифр является хорошим числом.

Например, пусть у Виталия любимые цифры 1 и 3, тогда число 12 — не является хорошим, а числа 13 или 311 являются. Также число 111 — замечательное, а число 11 — нет.

Теперь Виталий интересуется, сколько существует замечательных чисел длины ровно n. Так как количество таких чисел может быть довольно большим, он просит Вас посчитать остаток от деления этого количества на 1000000007 (109 + 7).

Под длиной числа подразумевается количество цифр в его десятичной записи без лидирующих нулей.

Входные данные
В первой строке записаны три целых числа: a, b, n (1 ≤ a < b ≤ 9, 1 ≤ n ≤ 106).

Выходные данные
Выведите единственное целое число — ответ на задачу по модулю 1000000007 (109 + 7).
"""
from sys import stdin


def main():
    mod = 10 ** 9 + 7
    a, b, n = map(int, stdin.read().split())
    f = [1] * (n + 1)
    for i in xrange(1, n + 1):
        f[i] = i * f[i - 1] % mod

    def ok(s):
        while s > 0:
            x = s % 10
            if x != a and x != b:
                return False
            s /= 10
        return True

    print f[n] * sum(pow(f[n - i] * f[i], mod - 2, mod) for i in xrange(n + 1) if ok(a*i + b*(n - i))) % mod

main()