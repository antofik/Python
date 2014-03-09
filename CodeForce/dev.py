def get_primes_and_factorization(N):
    lp = [0] * N
    pr = [0] * N
    p = 0
    for i in xrange(2, N):
        if not lp[i]:
            pr[p] = lp[i] = i
            p += 1
        for j in range(p):
            if pr[j] <= lp[i] and i * pr[j] < N - 1:
                lp[i * pr[j]] = pr[j]
            else:
                break
    return pr[:p], lp


pr, lp = get_primes_and_factorization(2*(10**6))

#print pr[-100:]

# 0.681
# 1.306
# 2.707
# 5.244