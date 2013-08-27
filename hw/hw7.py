# Name: Luis Morales
# Login: cs61a-3w
# TA: Sharad Vikram
# Section: 120
# Q1.

# Mutable rlist
def mutable_rlist():
    """A mutable rlist that supports push, pop, and setitem operations.

    >>> a = mutable_rlist()
    >>> a('push', 3)
    >>> a('push', 2)
    >>> a('push', 1)
    >>> a('setitem', 1, 4)
    >>> a('str')
    '<rlist (1, 4, 3)>'
    """
    contents = empty_rlist

    def setitem(index, value):
        k = 0
        list_items = []
        while k < index:
            list_items += [dispatch('pop')]
            k += 1
        dispatch('pop')
        dispatch('push', value)
        n = len(list_items)
        x = 0
        while x < n:
            dispatch('push', list_items[x])
            x += 1

    def dispatch(message, value=None, index=None):
        nonlocal contents
        if message == 'first':
            return first(contents)
        if message == 'rest':
            return rest(contents)
        if message == 'len':
            return len_rlist(contents)
        if message == 'getitem':
            return getitem_rlist(contents, value)
        if message == 'str':
            return str_rlist(contents)
        if message == 'pop':
            item = first(contents)
            contents = rest(contents)
            return item
        if message == 'push':
            contents = rlist(value, contents)
        if message == 'setitem':
            return setitem(value, index)

    return dispatch

def pair(x, y):
    def dispatch(m):
        if m == 0:
            return x
        elif m == 1:
            return y
    return dispatch

empty_rlist = None

def rlist(first, rest):
    return pair(first, rest)

def first(s):
    return s(0)

def rest(s):
    return s(1)

def len_rlist(s):
    if s == empty_rlist:
        return 0
    return 1 + len_rlist(rest(s))

def getitem_rlist(s, k):
    if k == 0:
        return first(s)
    return getitem_rlist(rest(s), k - 1)

def rlist_to_tuple(s):
    if s == empty_rlist:
        return ()
    return (first(s),) + rlist_to_tuple(rest(s))

def str_rlist(s):
    return '<rlist ' + str(rlist_to_tuple(s)) + '>'

# Q2.

class VendingMachine(object):
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('crab', 10)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.restock(2)
    'Current crab stock: 2'
    >>> v.vend()
    'You must deposit $10 more.'
    >>> v.deposit(7)
    'Current balance: $7'
    >>> v.vend()
    'You must deposit $3 more.'
    >>> v.deposit(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your crab and $2 change.'
    >>> v.deposit(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your crab.'
    >>> v.deposit(15)
    'Machine is out of stock. Here is your $15.'
    """
    def __init__(self, product, object_price):
        self.stock = 0
        self.product = product
        self.balance = 0
        self.object_price = object_price
    def vend(self):
        if self.balance >= self.object_price and self.stock >= 1:
            if self.stock == 1:
                print('Here is your',self.product+'.')
            if self.stock > 1:
                print('Here is your',self.product,'and','$'+str(self.balance-self.object_price), 'change.')
            self.stock -= 1
            self.balance = 0

        elif self.stock < 1:
            print('Machine is out of stock.')

        elif self.balance < self.object_price and self.stock >= 1:
            print('You must deposit','$'+str(self.object_price-self.balance),'more.')

    def deposit(self, cash_input):
        assert cash_input > 0, 'Cannot deposit negative amount'
        if self.stock < 1:
            print('Machine is out of stock. Here is your $'+str(cash_input)+'.')
            self.balance = 0
            return
        self.balance += cash_input
        print('Current balance:','$'+str(self.balance))
        return
    def restock(self, stock_input):
        assert stock_input > 0, 'Cannot restock negative amount'
        self.stock += stock_input
        print('Current',self.product,'stock:',self.stock)
        return



# Q3.

class MissManners(object):
    """A container class that only forward messages that say please.

    >>> v = VendingMachine('teaspoon', 10)
    >>> v.restock(2)
    'Current teaspoon stock: 2'
    >>> m = MissManners(v)
    >>> m.ask('vend')
    'You must learn to say please.'
    >>> m.ask('please vend')
    'You must deposit $10 more.'
    >>> m.ask('please deposit', 20)
    'Current balance: $20'  
    >>> m.ask('now will you vend?')
    'You must learn to say please.'
    >>> m.ask('please give up a teaspoon')
    'Thanks for asking, but I know not how to give up a teaspoon'
    >>> m.ask('please vend')
    'Here is your teaspoon and $10 change.'
    """
    def __init__(self, object1):
        self.object = object1    
    def ask(self, string, *args):
        please = 'please'
        if not string.startswith(please):
            print('You must learn to say please.')
            return
        specific_attr = string[len(please)+1:]
        if hasattr(self.object, specific_attr):
            return getattr(self.object, specific_attr)(*args)
        else:
            print('Thanks for asking, but I know not how to '+specific_attr)

# Q4.

class Account(object):
    """A bank account that allows deposits and withdrawals.

    >>> john = Account('John')
    >>> jack = Account('Jack')
    >>> john.deposit(10)
    10
    >>> john.deposit(5)
    15
    >>> john.interest
    0.02
    >>> jack.deposit(7)
    7
    >>> jack.deposit(5)
    12
    """

    interest = 0.02

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        """Increase the account balance by amount and return the new balance."""
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        """Decrease the account balance by amount and return the new balance."""
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance

class SecureAccount(Account):
    def __init__(self, account_holder, password):
        self.holder = account_holder
        self.password = password
        self.attempts = 0
        self.locked = False
        def withdraw(self, amount, password2=None):
            if password2 == None:
                return 'This account requires a password to withdraw'
            else:
                account.withdraw

        def secure_withdraw(self, amount, password1):
            if self.locked == False:
                if password1 == self.password:
                    account.withdraw
                else:
                    self.attempts += 1
                    if self.attempts >= 3:
                        self.locked = True
                        return
                    return 'Incorrect Password'
            else:
                return 'This account is locked'



import unittest

class SecureAccountTest(unittest.TestCase):
    """Test the SecureAccount class."""

    def setUp(self):
        self.account = SecureAccount('Alyssa P. Hacker', 'p4ssw0rd')

    def test_secure(self):
        acc = self.account
        acc.deposit(1000)
        self.assertEqual(acc.balance, 1000, 'Bank error! Incorrect balance')
        self.assertEqual(acc.withdraw(100),
                         'This account requires a password to withdraw')
        self.assertEqual(acc.secure_withdraw(100, 'p4ssw0rd'), 900,
                         "Didn't withdraw 100")
        self.assertEqual(acc.secure_withdraw(100, 'h4x0r'), 'Incorrect password')
        self.assertEqual(acc.secure_withdraw(100, 'n00b'), 'Incorrect password')
        self.assertEqual(acc.secure_withdraw(100, '1337'), 'Incorrect password')
        self.assertEqual(acc.balance, 900, 'Withdrew with bad password')
        self.assertEqual(acc.secure_withdraw(100, 'p4ssw0rd'),
                         'This account is locked')
        self.assertEqual(acc.balance, 900, 'Withdrew from locked account')

# Q5.

"*** YOUR CODE HERE ***"

class MoreSecureAccountTest(SecureAccountTest):
    """Test the MoreSecureAccount class."""

    def setUp(self):
        self.account = MoreSecureAccount('Alyssa P. Hacker', 'p4ssw0rd')
