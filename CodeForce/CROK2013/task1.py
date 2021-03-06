from sys import stdin

def main():
    stdin = open('test1_4') #-------------------------------------------------------------------------------

    n = int(stdin.readline())
    tasks = [(int(i), int(j)) for (i, j) in map(str.split, stdin.readlines())]

    stack = 0
    prev = 0
    max = 0
    for time, count in tasks:
        stack -= time - prev
        if stack < 0:
            stack = 0
        stack += count
        if stack > max:
            max = stack
        prev = time
    time = prev + stack

    print time, max

main()