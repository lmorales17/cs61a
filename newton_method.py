#this program is a non-functional attempt of newton's method (at least non-functional thus far)
square = lambda x: x*x

def sqrt(a):
	return find_root(square(x)-a)

def approx_deriv(f, delta=.000001):
	def deriv(x):
		return (f(x+delta)-f(x))/delta

	return deriv

def find_root(f):
	x = 1
	while not isclose(x):
		g = update(f)
		x = g(x)
	return x

def update(f):
	def guess(x):
		return (x-(f(x)/approx_deriv(x))
	return guess

def isclose(x):
	close_enough = .00001
	return (square(x)-a) < close_enough
