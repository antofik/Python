# coding=utf-8
"""
task_description
"""
from sys import stdin
import math


def get_primes_and_factorization(N):
    lp = [0] * (N + 1)
    pr = [0] * N
    pn = 0
    for i in xrange(2, N + 1):
        if not lp[i]:
            lp[i] = i
            pr.append(i)
            #pr[pn] = i
            #pn += 1
        for j, pr_j in enumerate(pr):
            if pr_j <= lp[i] and i * pr_j <= N:
                lp[i * pr_j] = pr_j
            else:
                break
    #pr = pr[:pn]
    return pr, lp


def main():
    k = int(stdin.readline())
    a = sorted(map(int, stdin.readline().split()))

    N = int(math.sqrt(sum(a)))
    MAX = max(N, max(a))
    pr, lp = get_primes_and_factorization(10**7)
    quit()

    cnt = [0] * (MAX + 2)
    for ai in a:
        cnt[ai] += 1
    for i in xrange(MAX - 1, 1, -1):
        cnt[i] += cnt[i + 1]

    for i in xrange(MAX, 1, -1):
        if lp[i] != i:
            cnt[lp[i]] += cnt[i]
        cnt[i / lp[i]] += cnt[i]

    rg = sum(a)
    lf = max(a)
    while rg != lf:
        mid = (rg + lf) // 2

        ok = True
        for prime in pr:
            s, k = 0, mid
            while k > 0:
                k //= prime
                s += k
            if s < cnt[prime]:
                ok = False
                break

        if ok:
            rg = mid
        else:
            lf = mid + 1

    print lf


main()