from collections import defaultdict
from sys import stdin


def main():
    stdin = open('test2_1') #-------------------------------------------------------------------------------

    values = [(int(i), int(j)) for (i, j) in map(str.split, stdin.readlines())]
    n, m = values[0]
    lines = values[1:]
    tree = defaultdict(int)
    for line in lines:
        x, y = line
        tree[x] += 1
        tree[y] += 1

    counts = {}
    for key in tree:
        value = tree[key]
        if value not in counts:
            counts[value] = 1
            if len(counts) > 2:
                print "unknown topology"
                exit()
        else:
            counts[value] += 1

    if len(counts) == 1 and (2 in counts):
        print "ring topology"
        exit()
    if len(counts) == 2 and (1 in counts) and (2 in counts) and counts[1] == 2 and counts[2] > 1:
        print "bus topology"
        exit()
    keys = sorted(counts.keys())
    if (len(keys) > 1) and (keys[0] == 1) and (keys[1] == n-1):
        print "star topology"
        exit()
    print "unknown topology"

main()

