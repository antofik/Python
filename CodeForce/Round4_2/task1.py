# coding=utf-8
"""
A. Арбуз
ограничение по времени на тест:1 second
ограничение по памяти на тест:64 megabytes
ввод:standard input
вывод:standard output

В один из жарких летних дней Петя и его друг Вася решили купить арбуз. Они выбрали самый большой и самый спелый, на их взгляд. После недолгой процедуры взвешивания весы показали w килограмм. Поспешно прибежав домой, изнемогая от жажды, ребята начали делить приобретенную ягоду, однако перед ними встала нелегкая задача. Петя и Вася являются большими поклонниками четных чисел, поэтому хотят поделить арбуз так, чтобы доля каждого весила именно четное число килограмм, при этом не обязательно, чтобы доли были равными по величине. Ребята очень сильно устали и хотят скорее приступить к трапезе, поэтому Вы должны подсказать им, удастся ли поделить арбуз, учитывая их пожелание. Разумеется, каждому должен достаться кусок положительного веса.
Входные данные

В первой и единственной строке входных данных записано целое число w (1 ≤ w ≤ 100) — вес купленного ребятами арбуза.
Выходные данные

Выведите YES, если ребята смогут поделить арбуз на две части, каждая из которых весит четное число килограмм, и NO в противном случае.
"""
from sys import stdin, exit


def task():
    w = int(stdin.readline())
    if w % 2 == 0 and w > 2:
        print 'YES'
    else:
        print 'NO'


task()


