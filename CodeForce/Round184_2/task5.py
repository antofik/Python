# coding=utf-8
"""
E. Игра со строкой
ограничение по времени на тест:2 секунды
ограничение по памяти на тест:256 мегабайт
ввод:standard input
вывод:standard output

Двое играют в следующую игру со строкой. Изначально у игроков есть некоторая строка s. Игроки делают ходы по очереди, а
игрок, который не может сделать очередной ход, проигрывает.

Перед началом игры строка записана на листочке, и каждая буква строки находится в отдельной ячейке.

Пример изначальной ситуации при s = «abacaba»


Ход игрока — это последовательность действий:

 Игрок выбирает один из доступных листочков, на котором записана некоторая строка. Обозначим ее t. Заметим, что
 изначально доступен только один листочек.
 Игрок выбирает в строке t = t1t2... t|t| символ в позиции i (1 ≤ i ≤ |t|) такой, что для некоторого целого
 положительного l (0 < i - l; i + l ≤ |t|) выполняются равенства: ti - 1 = ti + 1, ti - 2 = ti + 2, ..., ti - l = ti + l.
 Игрок вырезает ячейку с выбранным символом. В результате этой операции образуется три новых листочка, причем на
 первом будет записана строка t1t2... ti - 1, на втором — строка, состоящая из одного символа ti,
 на третьем — ti + 1ti + 2... t|t|.


Пример выполнения действия (i = 4) со строкой s = «abacaba»:

                                    abacaba => aba + c + aba


Ваша задача — определить, кто выиграет при оптимальной игре. Если при оптимальной игре выиграет тот, кто ходит первый,
определите позицию символа, который выгодно вырезать первым ходом первому. Если таких позиций несколько, найдите
минимально возможную.
Входные данные

В первой строке записана строка s (1 ≤ |s| ≤ 5000). Гарантируется, что строка s состоит только из строчных букв
латинского алфавита.
Выходные данные

Если выиграет второй игрок, то в единственной строке выведите «Second» (без кавычек). Иначе в первой строке выведите
«First» (без кавычек), а во второй строке — минимально возможный выигрышный ход — целое число i (1 ≤ i ≤ |s|).
"""
from sys import stdin


def task():
    value = stdin.readline()
    games = []
    counter = 0
    for i in xrange(1, len(value)-1):
        if value[i - 1] == value[i + 1]:
            counter += 1
        else:
            if counter > 0:
                games.append(counter)
            counter = 0
    if counter > 0:
        games.append(counter)
    max_game = max(games) if games else 0

    grundi = [0, 1, 1]
    for n in xrange(3, max_game + 1):
        s = {grundi[i] ^ grundi[n - i - 3] for i in xrange(0, n // 2 + 1)}
        s.add(grundi[n - 2])
        for i in xrange(n):
            if i not in s:
                grundi.append(i)
                break

    g = 0
    for game in games:
        g ^= grundi[game]
    print 'First' if g > 0 else 'Second'

    def check(n, g):
        if n < 3:
            return 0 if g == 0 else -1
        else:
            if grundi[n - 2] ^ g == 0:
                return 0
            for i in xrange(0, n - 2):
                if g ^ grundi[i] ^ grundi[n - i - 3] == 0:
                    return i + 1
            return -1

    cache = set()
    counter = 0
    delta = 0
    if g > 0:
        for i in xrange(1, len(value)-1):
            if value[i - 1] == value[i + 1]:
                if not delta:
                    delta = i + 1
                counter += 1
            else:
                if counter > 0:
                    if counter not in cache:
                        p = check(counter, grundi[counter] ^ g)
                        if p >= 0:
                            print delta + p
                            quit()
                        cache.add(counter)
                counter = 0
                delta = 0
        print delta + check(counter, grundi[counter] ^ g)

task()
