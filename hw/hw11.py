# Name: Luis Morales
# Login: cs61a-3w
# TA: Sharad Vikram
# Section: 120

BRACKETS = {('[', ']'): '+',
            ('(', ')'): '-',
            ('<', '>'): '*',
            ('{', '}'): '/'}
LEFT_RIGHT = {left:right for left, right in BRACKETS.keys()}
ALL_BRACKETS = set(b for bs in BRACKETS for b in bs)

# Q1.

def tokenize(line):
    """Convert a string into a list of tokens.

    >>> tokenize('<[2{12.5 6.0}](3 -4 5)>')
    ['<', '[', 2, '{', 12.5, 6.0, '}', ']', '(', 3, -4, 5, ')', '>']

    >>> tokenize('2.3.4')
    Traceback (most recent call last):
        ...
    ValueError: invalid token 2.3.4

    >>> tokenize('?')
    Traceback (most recent call last):
        ...
    ValueError: invalid token ?

    >>> tokenize('hello')
    Traceback (most recent call last):
        ...
    ValueError: invalid token hello

    >>> tokenize('<(GO BEARS)>')
    Traceback (most recent call last):
        ...
    ValueError: invalid token GO
    """
    token_list = []
    for elem in line:
        if coerce_to_number(elem):
            token_list.append(coerce_to_number(elem))
        else:
            token_list.append(elem)
    return token_list



def coerce_to_number(token):
    """Coerce a string to a number or return None.

    >>> coerce_to_number('-2.3')
    -2.3
    >>> print(coerce_to_number('('))
    None
    """
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            return None

# Q2.

def isvalid(tokens):
    """Return whether some prefix of tokens represent a valid Brackulator
    expression. Tokens in that expression are removed from tokens as a side
    effect.

    >>> isvalid(tokenize('([])'))
    True
    >>> isvalid(tokenize('([]')) # Missing right bracket
    False
    >>> isvalid(tokenize('[)]')) # Extra right bracket
    False
    >>> isvalid(tokenize('([)]')) # Improper nesting
    False
    >>> isvalid(tokenize('')) # No expression
    False
    >>> isvalid(tokenize('100'))
    True
    >>> isvalid(tokenize('<(( [{}] [{}] ))>'))
    True
    >>> isvalid(tokenize('<[2{12 6}](3 4 5)>'))
    True
    >>> isvalid(tokenize('()()')) # More than one expression is ok
    True
    >>> isvalid(tokenize('[])')) # Junk after a valid expression is ok
    True
    """
    def left_or_right(element):
        if element == '(' or element == '[' or element == '<' or element == '{':
            return 'L'
        elif element == ')' or element == ']' or element == '>' or element == '}':
            return 'R'
    numbers = 0
    validity_check = []
    for elem in tokens:
        if not coerce_to_number(elem):
            validity_check.append(left_or_right(elem))
        else:
            numbers += 1
    if len(validity_check) == 2:
        if numbers == 0:
            return True
        else:
            return False
    lefts = 0
    rights = 0

    for element in validity_check:
        if element == 'L':
            lefts += 1
        elif element == 'R':
            rights += 1


    if lefts != rights:
        return False
    neo_tester = []
    for thing in validity_check:
        if thing == 'L':
            neo_tester.append('L')
        else:
            if neo_tester.pop(0) == thing:
                return False
    return True

# Q3.

def brack_read(tokens):
    """Return an expression tree for the first well-formed Brackulator
    expression in tokens. Tokens in that expression are removed from tokens as
    a side effect.

    >>> brack_read(tokenize('100'))
    100
    >>> brack_read(tokenize('([])'))
    Pair('-', Pair(Pair('+', nil), nil))
    >>> print(brack_read(tokenize('<[2{12 6}](3 4 5)>')))
    (* (+ 2 (/ 12 6)) (- 3 4 5))
    >>> brack_read(tokenize('(1)(1)')) # More than one expression is ok
    Pair('-', Pair(1, nil))
    >>> brack_read(tokenize('[])')) # Junk after a valid expression is ok
    Pair('+', nil)

    >>> brack_read(tokenize('([]')) # Missing right bracket
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected end of line

    >>> brack_read(tokenize('[)]')) # Extra right bracket
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected )

    >>> brack_read(tokenize('([)]')) # Improper nesting
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected )

    >>> brack_read(tokenize('')) # No expression
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected end of line
    """
    n = len(tokens)
    k = 1
    read_brack = nil
    if tokens[0] is not type(int) or tokens[0] is not type(float):
        read_brack.first = BRACKETS[tokens[0]]
    else:
        return tokens[0]
    while k < n:
        if tokens[k] is not type(int) or not type(float):
            read_brack.rest = BRACKETS[tokens[k]]
        else:
            read_brack.rest = tokens[k]
        k += 1
        read_brack = read_brack.rest
    return read_brack



# Q4.

from urllib.request import urlopen

def puzzle_4():
    """Return the soluton to puzzle 4."""
    return 'peak'


class Pair(object):
    """A pair has two instance attributes: first and second.  For a Pair to be
    a well-formed list, second is either a well-formed list or nil.  Some
    methods only apply to well-formed lists.

    >>> s = Pair(1, Pair(2, nil))
    >>> s
    Pair(1, Pair(2, nil))
    >>> print(s)
    (1 2)
    >>> len(s)
    2
    >>> s[1]
    2
    >>> print(s.map(lambda x: x+4))
    (5 6)
    """
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return "Pair({0}, {1})".format(repr(self.first), repr(self.second))

    def __str__(self):
        s = "(" + str(self.first)
        second = self.second
        while isinstance(second, Pair):
            s += " " + str(second.first)
            second = second.second
        if second is not nil:
            s += " . " + str(second)
        return s + ")"

    def __len__(self):
        n, second = 1, self.second
        while isinstance(second, Pair):
            n += 1
            second = second.second
        if second is not nil:
            raise TypeError("length attempted on improper list")
        return n

    def __getitem__(self, k):
        if k < 0:
            raise IndexError("negative index into list")
        y = self
        for _ in range(k):
            if y.second is nil:
                raise IndexError("list index out of bounds")
            elif not isinstance(y.second, Pair):
                raise TypeError("ill-formed list")
            y = y.second
        return y.first

    def map(self, fn):
        """Return a Scheme list after mapping Python function FN to SELF."""
        mapped = fn(self.first)
        if self.second is nil or isinstance(self.second, Pair):
            return Pair(mapped, self.second.map(fn))
        else:
            raise TypeError("ill-formed list")

class nil(object):
    """The empty list"""

    def __repr__(self):
        return "nil"

    def __str__(self):
        return "()"

    def __len__(self):
        return 0

    def __getitem__(self, k):
        if k < 0:
            raise IndexError("negative index into list")
        raise IndexError("list index out of bounds")

    def map(self, fn):
        return self

nil = nil() # Assignment hides the nil class; there is only one instance


def read_eval_print_loop():
    """Run a read-eval-print loop for the Brackulator language."""
    global Pair, nil
    from scheme_reader import Pair, nil
    from scalc import calc_eval

    while True:
        try:
            src = tokenize(input('> '))
            while len(src) > 0:
              expression = brack_read(src)
              print(calc_eval(expression))
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D, etc.
            return

