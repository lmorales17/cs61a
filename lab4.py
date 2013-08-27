def add_ten_recur(n, x): 
	if n == 1:
		return x+10
	return 10+add_ten(n-1, x)

def add_ten_iter(n, x):
	k = 0
	total = 0
	while k < n:
		total, k = total+10, k+1
	return x+total

from math import pi

def sine(x):
	if x <= .00001:
		return x
	return (3*sine(x/3))-(4*(sine(x/3)**3))

def insect_paths(M, N):
	if M == 1 or N == 1:
		return 1
	return insect_paths(M, N-1)+insect_paths(M-1, N)