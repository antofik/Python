def get_primes(max_n=10 ** 7):
    """
    Returns list of prime numbers up to max
    """
    primes = []
    max_n += 1
    r = set(range(2, max_n))
    while r:
        n = min(r)
        r -= set(range(n, max_n, n))
        primes.append(n)
    return primes
