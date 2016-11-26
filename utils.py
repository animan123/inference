import random

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

def standardize (x):
	counter = random.randint (1000, 100000)
	for i, pred in enumerate (x):
		for j, arg in enumerate (pred["args"]):
			if isVariable (arg):
				x[i]["args"][j] = arg + str(counter)
	return x

def hasConstants (sub):
	if sub == {}:
		return True
	for x in sub:
		if isConstant (sub[x]):
			return True
	return False
