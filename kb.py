from input import get_cnf
from unify import isVariable

def get_kb (data):
	cnfs = []
	for s in data:
		new = get_cnf(s)
		for cnf in new:
			cnfs.append (cnf)
	counter = 0
	for i, t in enumerate (cnfs):
		counter += 1
		if t.op is None:
			for j, var in enumerate (t.pred["args"]):
				if isVariable (var):
					t.pred["args"][j] = var + str(counter)
		elif t.op == 'or':
			for k, child in enumerate (t.args):
				if child.op is not None:
					raise Exception ("Child of or is not None")
				for j, var in enumerate (child.pred["args"]):
					if isVariable (var):
						t.args[k].pred["args"][j] = var + str(counter)
		else:
			raise Exception ("Op is neither or nor None")
	return cnfs
