# Name: Luis Morales
# Login: cs61a-3w
# TA: Sharad Vikram
# Section: 120
# Q1.

def divide_by_fact(dividend, n):
    """Recursively divide dividend by the factorial of n.

    >>> divide_by_fact(120, 4)
    5.0
    """
    if n == 1:
        return dividend/n
    return divide_by_fact(dividend / n, n - 1)

# Q2.

def group(seq):
    """Divide a sequence of at least 12 elements into groups of 4 or
    5. Groups of 5 will be at the end. Returns a tuple of sequences, each
    corresponding to a group.

    >>> group(range(14))
    (range(0, 4), range(4, 9), range(9, 14))
    >>> group(tuple(range(17)))
    ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15, 16))
    """
    num = len(seq)
    assert num >= 12
    
    if num <= 24:
        number_of_fives = num%4
        ending_index = number_of_fives*5
        four_multiple_list = seq[:ending_index]
        counter1 = 0
        four_grouped_list = ()
        for numbers in four_multiple_list:
            counter1 += 1
            if counter1%4 == 0:
                four_grouped_list += tuple((range(seq[counter1-4], seq[counter1])))
        five_multiple_list = seq[ending_index:]
        counter2 = 0
        five_grouped_list = ()
        for numbers in five_multiple_list:
            counter2 += 1
            if counter2%5 == 0:
                five_grouped_list += tuple((range(seq[counter2-5], seq[counter2])))
        final_list = four_grouped_list+five_grouped_list
        return final_list

    return (group(seq[0:12]), group(seq[12:]))
"""

   ====
    ==
========== <--- spatula underneath this crust
 ========

    ||
    ||
   \||/
    \/

========== }
    ==     } flipped
   ====    }
 ========

"""

# Q3.

def partial_reverse(lst, start):
    """Reverse part of a list in-place, starting with start up to the end of
    the list.

    >>> a = [1, 2, 3, 4, 5, 6, 7]
    >>> partial_reverse(a, 2)
    >>> a
    [1, 2, 7, 6, 5, 4, 3]
    >>> partial_reverse(a, 5)
    >>> a
    [1, 2, 7, 6, 5, 3, 4]
    """
    reversing_list = lst[start:]
    reversed_list = []
    for k in reversing_list:
        reversed_list = [k] + reversed_list
    lst[start:] = reversed_list
    return




# Q4.

def index_largest(seq):
    """Return the index of the largest element in the sequence.

    >>> index_largest([8, 5, 7, 3 ,1])
    0
    >>> index_largest((4, 3, 7, 2, 1))
    2
    """
    assert len(seq) > 0
    largest_index = 0
    size_of_largest_index = 0
    n = range(0, len(seq))
    for index in n:
        if seq[index] > size_of_largest_index:
            size_of_largest_index = seq[index]
            largest_index = index
    return largest_index

# Q5.

def pizza_sort(lst):
    """Perform an in-place pizza sort on the given list, resulting in
    elements in descending order.

    >>> a = [8, 5, 7, 3, 1, 9, 2]
    >>> pizza_sort(a)
    >>> a
    [9, 8, 7, 5, 3, 2, 1]
    """
    n = len(lst)
    def foo(new_list, a):
        if a != n:
            largest_element = index_largest(new_list[a:])
            partial_reverse(new_list, a + largest_element)
            partial_reverse(new_list, a)
            foo(new_list, a+1)

    foo(lst, 0)

# Q6.

def make_accumulator():
    """Return an accumulator function that takes a single numeric argument and
    accumulates that argument into total, then returns total.

    >>> acc = make_accumulator()
    >>> acc(15)
    15
    >>> acc(10)
    25
    >>> acc2 = make_accumulator()
    >>> acc2(7)
    7
    >>> acc3 = acc2
    >>> acc3(6)
    13
    >>> acc2(5)
    18
    >>> acc(4)
    29
    """
    total = []
    def accumulate(addition):
        total.append(addition)
        return sum(total)
    return accumulate


# Q7.

def make_accumulator_nonlocal():
    """Return an accumulator function that takes a single numeric argument and
    accumulates that argument into total, then returns total.

    >>> acc = make_accumulator_nonlocal()
    >>> acc(15)
    15
    >>> acc(10)
    25
    >>> acc2 = make_accumulator_nonlocal()
    >>> acc2(7)
    7
    >>> acc3 = acc2
    >>> acc3(6)
    13
    >>> acc2(5)
    18
    >>> acc(4)
    29
    """
    total = 0
    def accumulate(addition):
        nonlocal total
        total += addition
        return total
    return accumulate


# Q8.

# Old version
def count_change(a, coins=(50, 25, 10, 5, 1)):
    if a == 0:
        return 1
    elif a < 0 or len(coins) == 0:
        return 0
    return count_change(a, coins[1:]) + count_change(a - coins[0], coins)

# Version 2.0
def make_count_change():
    """Return a function to efficiently count the number of ways to make
    change.

    >>> cc = make_count_change()
    >>> cc(500, (50, 25, 10, 5, 1))
    59576
    """
    "*** YOUR CODE HERE ***"

