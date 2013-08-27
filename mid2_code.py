def make_deposit():
	fraud = False
	contents = []
	def deposit(bucks):
		nonlocal fraud
		for serial in bucks:
			if serial in contents:
				fraud = True
			contents.append(serial)
		if fraud:
			return 'Fraud'
		return len(contents)
	return deposit