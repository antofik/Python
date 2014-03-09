# coding=utf-8
"""
B. Электронные таблицы
ограничение по времени на тест:10 seconds
ограничение по памяти на тест:64 megabytes
ввод:standard input
вывод:standard output

В популярных системах электронных таблиц (например, в программе Excel) используется следующая нумерация колонок. Первая колонка имеет номер A, вторая B и т.д. до 26-ой, которая обозначается буквой Z. Затем идут двухбуквенные обозначения: 27-ая обозначается как AA, 28-ая как AB, а 52-я обозначается парой AZ. Аналогично, следом за ZZ следуют трехбуквенные обозначения и т.д.

Строки обычно обозначаются целыми числами от 1. Номер ячейки получается конкатенацией обозначений для столбца и строки. Например, BC23 это обозначение для ячейки в столбце 55, строке 23.

Иногда используется другая форма записи: RXCY, где X и Y это целые числа, обозначающие номер строки и столбца, соответственно. Например, R23C55 это ячейка из примера выше.

Ваша задача написать программу, которая считывает последовательность обозначений ячеек и выводит каждое из обозначений в другой форме записи.
Входные данные

В первой строке записано целое число n (1 ≤ n ≤ 105), количество обозначений в тесте. Далее идет n строк, каждая из которых содержит обозначение. Известно, что все обозначения корректны, и не содержат ячейки с номерами строк или столбцов больших 106.
Выходные данные

Выведите n строк — каждая строка должна содержать обозначение ячейки в отличной форме записи.
Примеры тестов
Входные данные
2
R23C55
BC23
Выходные данные
BC23
R23C55
"""
from sys import stdin
import re

pattern1 = re.compile(r'[Rr](\d+)[Cc](\d+)')
pattern2 = re.compile(r'([^\d]+)(\d+)')


def to_abc(n):
    n = int(n)
    result = ''
    while n > 0:
        v = n % 26
        n /= 26
        if v > 0:
            result = chr(ord('A') + v - 1) + result
        else:
            n -= 1
            result = 'Z' + result
    return result


def to_int(abc):
    result = 0
    i = 1
    for ch in list(abc.upper())[::-1]:
        result += (1 + ord(ch) - ord('A')) * i
        i *= 26
    return result


def switch(value):
    m = pattern1.match(value)
    if m:
        row, column = m.groups()
        value = '%s%s' % (to_abc(column), row)
    else:
        m = pattern2.match(value)
        column, row = m.groups()
        value = 'R%sC%s' % (row, to_int(column))
    return value

stdin.readline()
for value in [switch(value.strip()) for value in stdin.readlines()]:
    print value