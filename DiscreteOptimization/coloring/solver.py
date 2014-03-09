#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict, Counter
import operator
import os
import random
from subprocess import Popen, PIPE


def solveWithCpp(inputData):
    tmpFileName = 'tmp.data'
    tmpFile = open(tmpFileName, 'w')
    tmpFile.write(inputData)
    tmpFile.close()

    #process = Popen(["""C:/Users/anton/Documents/visual studio 2010/Projects/ConsoleApplication8/ConsoleApplication8/bin/Debug/ConsoleApplication8.exe""", tmpFileName], stdout=PIPE)
    process = Popen([r"""C:\Users\anton\Documents\visual studio 2013\Projects\GraphColoring\Debug\GraphColoring.exe""", tmpFileName], stdout=PIPE)
    (stdout, stderr) = process.communicate()

    os.remove(tmpFileName)

    value = stdout.strip()

    print value
    return value


def solveIt(inputData):
    """
    task 1: gc_50_3, answer=6
    task 2: gc_70_7, answer=17
    task 3: gc_100_5, answer=15
    task 4: gc_250_9, answer=73
    task 5: gc_500_1, answer=12?
    task 6: gc_1000_5, answer=83?
    """
    return solveWithCpp(inputData)


    lines = inputData.split('\n')

    count, _ = map(int, lines[0].split())

    vertex = defaultdict(set)
    edges = [map(int, line.split()) for line in lines[1:] if line]
    for i, j in edges:
        vertex[i].add(j)
        vertex[j].add(i)

    ranks = sorted([(i, len(vertex[i])) for i in xrange(count)], key=operator.itemgetter(1), reverse=True)

    solver = Solver(count, edges, vertex, ranks)
    solver.solve()

    return '%s %s\n%s' % (solver.color_count, 0, ' '.join(map(str, solver.get_solution())))


class Solver(object):
    def __init__(self, count, edges, vertex, ranks):
        self.count = count
        self.edges = edges
        self.vertex = vertex
        self.ranks = ranks
        self.color_count = 0
        self.colors = []
        self.nodes = []
        self.unused_colors = list(reversed(range(count)))
        for i in xrange(count):
            node = Node(i, count, self.nodes, self.vertex[i])
            self.nodes.append(node)
        self.get_rankest_notready_node_index = self.get_rankest_notready_node_index_generator()

    def get_next_color(self):
        self.color_count += 1
        color = self.unused_colors.pop()
        self.colors.append(color)
        return color

    def get_solution(self):
        return [node.color for node in self.nodes]

    def solve(self):
        #find initial solution
        while self.assign_color_for_next_rankest_node():
            pass

        for node in self.nodes:
            node.max_colors = self.color_count - 1

        while True:
            #choosing color to reduce
            #for color in xrange(self.color_count):
            counter = Counter(self.get_solution())
            color = sorted(counter.iteritems(), key=operator.itemgetter(1))[0][0]

            #saving solution
            for node in self.nodes:
                node.save()

            self.reduce_color(color)
            max_iteration = 10000
            iteration = 0
            while not self.try_to_use_available_colors() and iteration < max_iteration:
                iteration += 1

            if iteration < max_iteration:
                self.color_count -= 1
                print 'Succeeded to reduce color count to %s in %s iterations' % (self.color_count, iteration)
            else:
                print 'Failed to reduce color count'
                for node in self.nodes:
                    node.rollback()
                break

    def get_rankest_notready_node_index_generator(self):
        for i, _ in self.ranks:
            if not self.nodes[i].color > -1:
                yield i
        yield -1

    def assign_color_to_node(self, node):
        for color in self.colors:
            if node.can_set_color(color):
                node.set_color(color)
                break
        else:
            node.set_color(self.get_next_color())

    def assign_color_for_next_rankest_node(self):
        #get node with highest rank (not colored yet)
        rankest_node_index = self.get_rankest_notready_node_index.next()
        if rankest_node_index == -1:
            return False
        rankest_node = self.nodes[rankest_node_index]
        self.assign_color_to_node(rankest_node)

        #setting color for all adjacent nodes
        for node in [self.nodes[i] for i in self.vertex[rankest_node_index] if not self.nodes[i].color > -1]:
            self.assign_color_to_node(node)

        return True

    def swap_color(self, color):
        for node in self.nodes:
            node.swap_color(color)

    def reduce_color(self, color):
        self.swap_color(color)
        for node in self.nodes:
            node.reduce_color()

    def try_to_use_available_colors(self):
        ok = True
        for node in self.nodes:
            if not node.color > -1:
                if not node.try_to_use_available_colors():
                    ok = False
        return ok


class Node(object):
    def __init__(self, index, max_colors, nodes, adjacent):
        self.index = index
        self.colors = set(range(max_colors))
        self.nodes = nodes
        self.adjacent = adjacent
        self.color = -1
        self.max_colors = max_colors

    def save(self):
        self.backup = self.color

    def rollback(self):
        self.color = self.backup

    def swap_color(self, color):
        if self.color == color:
            self.color = self.max_colors
        elif self.color == self.max_colors:
            self.color = color

    def reduce_color(self):
        if self.color == self.max_colors:
            self.color = -1
        self.max_colors -= 1

    def try_to_use_available_colors(self):
        self.update_available_colors()
        if self.colors:
            self.color = random.choice(list(self.colors))
            return True
        else:
            self.color = random.randint(0, self.max_colors - 1)
            for neigbour in self.adjacent:
                node = self.nodes[neigbour]
                if node.color == self.color:
                    node.color = -1
            return False

    def update_available_colors(self):
        colors = [self.nodes[i].color for i in self.adjacent if self.nodes[i].color > -1]
        colors = set(range(self.max_colors)) - set(colors)
        if self.color > -1 and self.color in colors:
            colors.remove(self.color)
        self.colors = colors

    def can_remove_color(self, color):
        return (color != self.color and self.color > -1) or color not in self.colors or len(self.colors) > 1

    def can_set_color(self, color):
        if color not in self.colors:
            return False
        for neigbour in self.adjacent:
            if not self.nodes[neigbour].can_remove_color(color):
                return False
        return True

    def set_color(self, color):
        self.color = color
        self.colors = {color}
        for neigbour in self.adjacent:
            self.nodes[neigbour].remove_color(color)

    def remove_color(self, color):
        if color in self.colors:
            self.colors.remove(color)


def main():
    import sys
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = inputDataFile.read()
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file, i.e. python solver.py ./data/gc_4_1'

if __name__ == '__main__':
    main()

