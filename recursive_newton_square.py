def newtonsquare(x):

	def f(x, estimate):
		if abs(x-estimate ** 2) <= .000000001:
			return estimate
		else:
			return f(x, (estimate + x / estimate) / 2)

	return f(x, 1.0)

