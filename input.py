from term import term

def get_operator (op):
	if op == '=':
		return 'imply'
	if op == '|':
		return 'or'
	if op == '&':
		return 'and'
	raise Exception ("Invalid operator " + op)

def isUpper (x):
	return x>='A' and x<='Z'

def get_pred_dict (pred_string):
	first_bracket = pred_string.index('(')
	pred_name = pred_string[:first_bracket]
	pred_args = pred_string[first_bracket+1:-1].split(',')
	pred_args = [x.replace('(','') for x in pred_args]
	pred_args = [x.replace(')','') for x in pred_args]
	return {
		"name": pred_name,
		"args": pred_args
	}

def preprocess (s):
	s = s.replace ('=>', '=')
	s = s.replace (' ', '')
	t = ''
	i = 0
	while i < len(s):
		if isUpper (s[i]) and s[i-1] != '~' and not isUpper(s[i-1]):
			j = s.index(')', i+1)
			x = '(' + s[i:j+1] + ')'
			t += x
			i = j+1
		else:
			t += s[i]
			i += 1
	return t

def process (s):
	s = s[1:-1]
	#print len(s), s
	if (s[0]=='~' and isUpper(s[1])) or (isUpper(s[0])):
		#print "part 1"
		if s[0]  == '~':
			s = s[1:]
			truth = False
		else:
			truth = True
		return term(truth=truth, pred=get_pred_dict (s))

	elif s[0]=='~':
		#print "part 2"
		return term(truth=False, args=[process(s[1:])])

	else:
		#print "part 3"
		substring = ''
		args = []
		count = 0
		op = None
		for c in s:
			if c in ['&', '|', '='] and count == 0:
				op = c
			else:
				substring += c
			if c == '(':
				count += 1
			if c == ')':
				count -= 1
			if count == 0:
				if (c == ')' and op is not None) or c in ['&', '|', '=']:
					#print "Sending substring: ", substring
					args.append (process(substring))
					substring = ''
		return term(op=get_operator(op), args=args)

def get_cnf (s):
	s = preprocess (s)
	t = process(s)
	t.simplify ()
	return t.get_cnf ()

if __name__ == '__main__':
	#s = '((AA(x, y)|(~BB(p, q)))=>(CC(x)|DD(p)))'
	#s = '(~(~(~(~(~A(x))))))'
	#s = '((A(x)=>B(x))=>C(x))'
	#s = 'Q(Alice, Bob)'
	s = '((~(Parent(x,y) & Ancestor(y,z))) | Ancestor(x,z))'
	#s = '(~(Parent(x,y) & Ancestor(y,z)))'
	s = preprocess (s)
	t = process (s)
	#t.show ()
	t.simplify ()
	#t.show ()

	cnf = t.get_cnf ()
	for x in cnf:
		print x
	
