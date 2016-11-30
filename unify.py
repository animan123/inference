from utils import isVariable, isConstant

def unify_all (x, y, sub):
	if sub is None:
		return sub
	if x == y:
		return sub
	if isVariable(x):
		return unify_var (x, y, sub)
	if isVariable(y):
		return unify_var (y, x, sub)
	if type(x)==type([]) and type(y)==type([]):
		return unify_all (
			x[1:],
			y[1:],
			unify_all (
				x[0], y[0], sub
			)
		)
	return None

def unify_var (var, x, sub):
	if var in sub:
		return unify_all (sub[var], x, sub)
	if x in sub:
		return unify_all (var, sub[x], sub)
	sub[var] = x
	return sub

def unify (predicate1, predicate2, opposites=True):
	if predicate1["name"] != predicate2["name"] or len(predicate1["args"]) != len(predicate2["args"]):
		return None
	if opposites:
		if predicate1["truth"] == predicate2["truth"]:
			return None
	else:
		if predicate1["truth"] != predicate2["truth"]:
			return None
	args1 = predicate1["args"]
	args2 = predicate2["args"]
	return unify_all (args1, args2, {})

def simpler_unify (predicate1, predicate2):
	if predicate1["name"] != predicate2["name"] or len(predicate1["args"]) != len(predicate2["args"]) or predicate1["truth"] != predicate2["truth"]:
		return None
	args1 = predicate1["args"]
	args2 = predicate2["args"]
	sub = {}
	for x, y in zip(args1, args2):
		if isVariable(x) and isConstant(y):
			return None
		if isConstant(x) and isVariable(y):
			return None
		if isConstant(x) and x!=y:
			return None
		if isVariable(x):
			sub[x] = y
	return sub

def Consistent (s1, s2):
	for x in s1:
		if x in s2 and s1[x] != s2[x]:
			return False
	for x in s2:
		if x in s1 and s1[x] != s2[x]:
			return False
	return True

def isSame (sentence1, sentence2, sub={}):
	if sentence1 == [] and sentence2 == []:
		return True
	if len(sentence1) != len(sentence2):
		return False
	for i in range (len(sentence1)):
		for j in range(len(sentence2)):
			sub2 = simpler_unify (sentence1[i], sentence2[j])
			#print sentence1[i]
			#print sentence2[j]
			#print sub2
			#xxx = input()
			if sub2 is not None and Consistent(sub, sub2):
				x = sentence1[:i] + sentence1[i+1:]
				y = sentence2[:j] + sentence2[j+1:]
				result = isSame (x, y, dict(sub.items()+sub2.items()))
				if result:
					return True
	return False

if __name__ == '__main__':
	sentence1 = [
		{
			"name": "Friend",
			"args": ['y1', 'x1'],
			"truth": False
		},
		{
			"name": "Friend",
			"args": ['Sid', 'y1'],
			"truth": False
		},
		{
			"name": "Friend",
			"args": ['x1', 'y2'],
			"truth": False
		},
		{
			"name": "Friend",
			"args": ['y2', 'Hanam'],
			"truth": False
		}
	]
	sentence2 = [
		{
			"name": "Friend",
			"args": ['z22', 'Hanam'],
			"truth": False
		},
		{
			"name": "Friend",
			"args": ['y11', 'z22'],
			"truth": False
		},
		{
			"name": "Friend",
			"args": ['Sid', 'z11'],
			"truth": False
		},
		{
			"name": "Friend",
			"args": ['z11', 'y11'],
			"truth": False
		}
	]
	print isSame (sentence1, sentence2)
