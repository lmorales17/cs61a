# Name: Luis Morales, James Musk
# Login: cs61a-3w, cs61a-wb
# TA: Sharad Vikram
# Section: 120

def square(x):
    """Return x squared."""
    return x * x

# Q1.

def product(n, term):
    """Return the product of the first n terms in a sequence.

    term -- a function that takes one argument

    >>> product(4, square)
    576
    """
    k = 1 #k is a placeholder value that starts at 1 and goes to n
    total = 1 #total is a value equal to the current product total and starts at 1
    while k <  n:
        x = term(k)
        k = k+1
        total = (total*x)

    return total*term(k)
                


def factorial(n):
    """Return n factorial by calling product.

    >>> factorial(4)
    24
    """
    def identity(x): #I defined an identity function that does nothing
        return x
    return product(n, identity)
    

# Q2.

def accumulate(combiner, start, n, term):
    """Return the result of combining the first n terms in a sequence."""
    from operator import add
    k = 1
    total = 1
    if combiner == add:
        total = 0
    while k != n:
        k, x = k+1, term(k)
        total = combiner(total, x)

    return add(combiner(total, term(k)), start)
        


def summation_using_accumulate(n, term):
    """An implementation of summation using accumulate.

    >>> summation_using_accumulate(4, square)
    30
    """
    from operator import add
    return accumulate(add, 0, n, term)

def product_using_accumulate(n, term):
    """An implementation of product using accumulate.

    >>> product_using_accumulate(4, square)
    576
    """
    from operator import mul
    return accumulate(mul, 0, n, term)

# Q3.

def double(f):
    """Return a function that applies f twice.

    f -- a function that takes one argument

    >>> double(square)(2)
    16
    """
    def compose1(f, g):
        def h(x):
            return f(g(x))
        return h
    doubled = compose1( f, f)
    return doubled
                
    
        


# Q4.

def repeated(f, n):
    """Return the function that computes the nth application of f.

    f -- a function that takes one argument
    n -- a positive integer

    >>> repeated(square, 2)(5)
    625
    >>> repeated(square, 4)(5)
    152587890625
    """
    def compose1(f, g):
        def h(x):
            return f(g(x))
        return h
    k = 1
    multi = compose1( f, f)
    final_value = f
    while k != n:
        final_value = multi
        k, multi = k+1, compose1(f, multi)
    return final_value



def compose1(f, g):
    """Return a function h, such that h(x) = f(g(x))."""
    def h(x):
        return f(g(x))
    return h

# Q5.

def zero(f):
    return lambda x: x

def successor(n):
    return lambda f: lambda x: f(n(f)(x))


def one(f):
    """Church numeral 1."""
    "*** YOUR CODE HERE ***"

def two(f):
    """Church numeral 2."""
    "*** YOUR CODE HERE ***"

def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    """
    "*** YOUR CODE HERE ***"

def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> three = successor(two)
    >>> church_to_int(add_church(two, three))
    5
    """
    "*** YOUR CODE HERE ***"

def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> three = successor(two)
    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    "*** YOUR CODE HERE ***"

def pow_church(m, n):
    """Return the Church numeral for m ** n, for Church numerals m and n.

    >>> three = successor(two)
    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    "*** YOUR CODE HERE ***"
