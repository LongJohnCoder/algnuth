"""
Jacobi symbol, Solovay–Strassen primality test and sieve of Eratosthenes
"""

from random import randrange
from math import gcd


def expsign(sign, exp):
    """
    optimization of sign ** exp
    """
    if sign == 1:
        return 1
    assert sign == -1
    return -1 if exp % 2 else 1


def jacobi(m, n):
    """
    Jacobi's symbol
    the rule for (-1/n) is not used
    """
    assert n % 2
    if m == 2:
        if n % 8 in [1, 7]:
            return 1
        return -1
    m %= n
    q = 0
    while m & 1 == 0:
        m >>= 1
        q += 1
    if m == 1:
        return expsign(jacobi(2, n), q)
    return (expsign(jacobi(2, n), q)
            * (-1 if (n % 4 == 3) and (m % 4 == 3) else 1)
            * jacobi(n, m))


def solovay_strassen(n, prec=50):
    """
    Solovay–Strassen primality test
    with error probability less than 2^-prec
    """
    if n == 1:
        return False
    if n % 2 == 0:
        return n == 2
    e = (n - 1) // 2
    for _ in range(prec):
        x = randrange(1, n)
        if gcd(x, n) != 1 or pow(x, e, n) != (jacobi(x, n) % n):
            return False
    return True


def sieve(limit=10**5):
    """
    Sieve of Eratosthenes
    """
    l = [True] * (limit + 1)
    l[0] = l[1] = 0
    next = 2
    while next < limit:
        for k in range(2, limit // next + 1):
            l[k * next] = False
        next += 1
        while next < limit and not l[next]:
            next += 1
    return [i for i in range(limit) if l[i]]


def test_solovay_strassen(limit=10**5):
    """
    Runs in ~20s with limit = 10^5
    """
    primes = set(sieve(limit))
    for i in range(limit):
        assert (i in primes) == solovay_strassen(i)


if __name__ == '__main__':
    test_solovay_strassen(10**3)
    p = 12779877140635552275193974526927174906313992988726945426212616053383820179306398832891367199026816638983953765799977121840616466620283861630627224899026453
    q = 12779877140635552275193974526927174906313992988726945426212616053383820179306398832891367199026816638983953765799977121840616466620283861630627224899027521
    n = p * q
    assert solovay_strassen(p)
    assert solovay_strassen(q)
    assert not solovay_strassen(n)
