def sum(n):
	if n == 1:
		return 1
	return n + sum(n-1)

def ab_plus_c(a, b, c):
	if a == 1:
		return b+c
	if b == 1:
		return a+c
	if b == 1 and a ==1:
		return c+1
	return ab_plus_c(a-1, b-1, c)

def summation( n, term): #where term is a function
	if n == 0:
		return 0
	return term(n)+summation(n-1, term)



def hailstone(n):
	print(n)
	if n == 1:
		return 1
	if n%2 == 0:
		return 1+hailstone(n//2)
	else:
		return 1+hailstone((n*3)+1)

def compose1(f, g):
	"""Return a function h, such that h(x) = f(g(x))."""
	def h(x):
		return f(g(x))
	return h

def repeated(f, n):
	if n == 0:
		return f
	return compose1(f, repeated(f, n-1))

def iter_factorial(n):
	k = 0
	while k <n:










