class IteratorIterator(object):
	def __init__(self):
		self.start = 0

	def __next__(self):
		temp = self.start
		self.start += 1
		return NaturalIterator(temp)

class NaturalIterator(object):
	def __init__(self, start=0):
		self.start = start
		
	def __next__(self):
		temp = self.start
		self.start += 1
		return temp
		
	def __iter__(self):
		return self

def natlistgen(end):
	start = [1]
	while start[-1] < end:
		yield start
		start.append(start[-1]+1)

def fib_gen():
	prev = 0
	curr = 1
	while True:
		yield curr
		prev, curr = curr, prev+curr

def even_gen():
	start = 2
	while True:
		yield start
		start += 2

def intersect(iter1, iter2):
	temp1 = next(iter1)
	temp2 = next(iter2)
	while True:
		if temp1 == temp2:
			result = temp1
			temp1 = next(iter1)
			temp2 = next(iter2)
			yield result
		elif temp1 < temp2:
			temp1 = next(iter1)
		else:
			temp2 = next(iter2)


