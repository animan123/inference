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

def unify (predicate1, predicate2):
	if predicate1["name"] != predicate2["name"] or len(predicate1["args"]) != len(predicate2["args"]) or (predicate1["truth"] == predicate2["truth"]):
		return None
	args1 = predicate1["args"]
	args2 = predicate2["args"]
	return unify_all (args1, args2, {})

if __name__ == '__main__':
	pred1 = {
		"name": "AA",
		"args": ['x1', 'John'],
	}
	pred2 = {
		"name": "AA",
		"args": ['Mary', 'y1'],
	}
	print unify(pred1, pred2)
