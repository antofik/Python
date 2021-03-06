# coding=utf-8
"""
B. Наименее круглый путь
ограничение по времени на тест:5 seconds
ограничение по памяти на тест:64 megabytes
ввод:standard input
вывод:standard output

Задана квадратная матрица n × n, состоящая из неотрицательных целых чисел. Вам надо найти такой путь на ней, который
 начинается в левой верхней ячейке матрицы;
 каждой следующей ячейкой имеет правую или нижнюю от текущей;
 заканчивается в правой нижней клетке.


Кроме того, если перемножить все числа вдоль пути и посмотреть на получившиеся произведение, то это число должно быть как можно менее «круглым». Иными словами оно должно заканчиваться на наименьшее возможное количество нулей.
Входные данные

В первой строке содержится целое число n (2 ≤ n ≤ 1000), n — размер заданной матрицы. Далее в n строках содержатся элементы матрицы (целые неотрицательные числа, не превосходящие 109).
Выходные данные

В первую строку выведите искомое наименьшее количество концевых нулей в произведении чисел вдоль пути. Во вторую выведите сам путь.
Примеры тестов
Входные данные
3
1 2 3
4 5 6
7 8 9
Выходные данные
0
DDRR
"""
from sys import stdin


def weight(value, k):
    n = 0
    while (value % k) == 0:
        value /= k
        n += 1
    return n


def find_path(m, k, n):
    l = [[weight(m[j][i], k) for j in xrange(n)] for i in xrange(n)]
    for i in xrange(n - 1):
        l[i + 1][0] += l[i][0]
        l[0][i + 1] += l[0][i]
    for j in xrange(1, n):
        for i in xrange(1, n):
            l[j][i] += min(l[j][i-1], l[j-1][i])
    w = l[n - 1][n - 1]
    path = []
    x = y = n - 1
    while x > 0 or y > 0:
        if (x > 0 and y > 0 and l[x - 1][y] < l[x][y - 1]) or y == 0:
            path.append('R')
            x -= 1
        else:
            path.append('D')
            y -= 1
    del l
    return w, path


def main():
    n = int(stdin.readline())
    m = [map(int, line) for line in map(str.split, stdin.readlines())]
    zero = None
    for y in xrange(n):
        for x in xrange(n):
            if m[y][x] == 0:
                m[y][x] = 10
                zero = (x, y)

    w, path = min(find_path(m, 2, n), find_path(m, 5, n))

    if w > 1 and zero:
        d, l = zero
        print 1, '\n', 'R' * d + 'D' * (n - 1) + 'R' * (n - d - 1)
    else:
        print w, '\n', ''.join(path[::-1])

main()