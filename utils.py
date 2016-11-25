def isVariable (x):
	if not type(x) == type(''):
		return False
	if not (x[0]>='a' and x[0]<='z'):
		return False
	for c in x[1:]:
		if not (c>='0' and c<='9'):
			return False
	return True

def isConstant (x):
	return not isVariable (x)
