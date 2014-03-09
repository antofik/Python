# coding=utf-8
"""
task_description
"""
from sys import stdin

n = int(stdin.readline())
m = map(int, stdin.readline().split())
m.sort()
a1 = []
a2 = []
a3 = []
a_p = []
a_m = []
a_z = []

for i in m:
    if i > 0:
        a_p.append(i)
    elif i < 0:
        a_m.append(i)
    else:
        a_z.append(i)

a1 = a_m[:1]
a3 = a_z
if len(a_p) > 0:
    a2 = a_p
    a3.extend(a_m[1:])
else:
    a2 = a_m[1:3]
    a3.extend(a_m[3:])
for a in [a1, a2, a3]:
    print len(a), ' '.join(map(str, a))