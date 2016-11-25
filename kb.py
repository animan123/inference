from input import get_cnf

def get_kb (data):
	cnfs = []
	for s in data:
		new = get_cnf(s)
		for cnf in new:
			cnfs.append (cnf)
	return cnfs
