# coding=utf-8
"""
C. Крестики-нолики
ограничение по времени на тест:1 second
ограничение по памяти на тест:64 megabytes
ввод:standard input
вывод:standard output

Все, наверное, знакомы с игрой крестики-нолики. Правила в самом деле очень просты. Игроки по очереди ставят на свободные клетки поля 3 × 3 знаки (один всегда крестики, другой всегда нолики). Первый, выстроивший в ряд три своих фигур по вертикали, горизонтали или диагонали, выигрывает и игра заканчивается. Первый ход делает игрок, ставящий крестики. В том случае, если все поле заполнено, но никакие три фигуры в ряд не стоят, то объявляется ничья.

Вам задано поле 3 × 3, на котором каждая клетка свободна или занята крестиком или ноликом. Ваша задача указать игрока (first или second), ход которого ожидается или вывести один из четырех вердиктов:
illegal — если заданная игровая позиция не может появиться в ходе игры, т.е. является некорректной;
the first player won — если в заданной игровой позиции первый игрок только что победил;
the second player won — если в заданной игровой позиции второй игрок только что победил;
draw — если в заданной игровой позиции только что наступила ничья.

Входные данные

Входные данные состоят из трех строк, каждая из которых содержит по три символа: «.», «X» или «0» (точку, заглавную букву X или ноль).
Выходные данные

Выведите один из шести вердиктов: first, second, illegal, the first player won, the second player won или draw.
"""
from collections import defaultdict
from sys import stdin, exit

board = defaultdict(int)

who = 0
count = 0
for y, line in enumerate(stdin.readlines(), start=1):
    for x, value in enumerate(list(line.strip()), start=1):
        if value == 'X':
            board[x, y] = 1
            who += 1
            count += 1
        elif value == '0':
            board[x, y] = 2
            who -= 1
            count += 1

if who < 0 or who > 1:
    print 'illegal'
    exit()
who += 1

winner = 0
win_type = 0
win_count = 0
combinations = [
    (1, board[1, 1], board[1, 2], board[1, 3]),
    (1, board[2, 1], board[2, 2], board[2, 3]),
    (1, board[3, 1], board[3, 2], board[3, 3]),
    (2, board[1, 1], board[2, 1], board[3, 1]),
    (2, board[1, 2], board[2, 2], board[3, 2]),
    (2, board[1, 3], board[2, 3], board[3, 3]),
    (3, board[1, 1], board[2, 2], board[3, 3]),
    (4, board[1, 3], board[2, 2], board[3, 1]),
]
for kind, c1, c2, c3 in combinations:
    if c1 == c2 == c3 and c1 > 0:
        win_count += 1
        if winner > 0 and winner != c1 or win_count > 2 or kind == win_type:
            print 'illegal'
            exit()
        winner = c1
        win_type = kind

if winner == who:
    print 'illegal'
    exit()
if winner == 1:
    print 'the first player won'
    exit()
elif winner == 2:
    print 'the second player won'
    exit()

if count == 9:
    print 'draw'
    exit()

if who == 2:
    print 'second'
else:
    print 'first'