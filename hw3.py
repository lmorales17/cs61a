# Name: Luis Morales
# Login: cs61a-3w
# TA: Sharad Vikram
# Section: 120
# Q1.

def smooth(f, dx):
    """Returns the smoothed version of f, g where

    g(x) = (f(x - dx) + f(x) + f(x + dx)) / 3

    >>> square = lambda x: x ** 2
    >>> round(smooth(square, 1)(0), 3)
    0.667
    """
    return lambda x: (f(x-dx) + f(x) + f(x+dx)) / 3

def n_fold_smooth(f, dx, n):
    """Returns the n-fold smoothed version of f

    >>> square = lambda x: x ** 2
    >>> round(n_fold_smooth(square, 1, 3)(0), 3)
    2.0
    """
    def many_smooth(x):
        apply_many = lambda x: (f(x-dx)+f(x)+f(x+dx))/3
        k = 0
        while k < n:
            x = apply_many(x)
            k = k+1
        return x
    return many_smooth
    
# Q2.

def iterative_continued_frac(n_term, d_term, k):
    """Returns the k-term continued fraction with numerators defined by n_term
    and denominators defined by d_term.

    >>> # golden ratio
    ... round(iterative_continued_frac(lambda x: 1, lambda x: 1, 8), 3)
    0.618
    >>> # 1 / (1 + (2 / (2 + (3 / (3 + (4 / 4))))))
    ... round(iterative_continued_frac(lambda x: x, lambda x: x, 4), 6)
    0.578947
    """
    i = 0
    t = 0
    while k > 0:
        t = n_term(k)/(d_term(k)+t)
        k = k-1
    return t

def recursive_continued_frac(n_term, d_term, k):
    """Returns the k-term continued fraction with numerators defined by n_term
    and denominators defined by d_term.

    >>> # golden ratio
    ... round(recursive_continued_frac(lambda x: 1, lambda x: 1, 8), 3)
    0.618
    >>> # 1 / (1 + (2 / (2 + (3 / (3 + (4 / 4))))))
    ... round(recursive_continued_frac(lambda x: x, lambda x: x, 4), 6)
    0.578947
    """
    def foo(n_term, d_term, k, i):
        if k == i:
            return n_term(k)/d_term(k)
        else:
            return (n_term(i)/(d_term(i) + foo(n_term, d_term, k, i + 1))
    return foo(n_term(i), d_term(i), k, 1)

# Q3.

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    """
    if n <= 3:
        return n
    else:
        return g(n-1)+2*(g(n-2))+3*(g(n-3))


def g_iter(n):
    """Return the value of G(n), computed iteratively.
    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    """
    k = 0
    t = 0
    z = n
    if n <= 3:
        return n
    while k < (n-3):
        k += 1
        x = (z-1)+2*(z-2)+3*(z-3)
        z -= 1
        t = t + x
    if n > 4:
        return t - 4
    return t


# Q4.

from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    """
    return YOUR_EXPRESSION_HERE
