def product (ar_list):
	if not ar_list:
		yield ()
	else:
		for a in ar_list[0]:
			for prod in product (ar_list[1:]):
				yield (a,) + prod

class term:
	def __init__ (self, truth=True, op=None, args=[], pred=None):
		self.truth = truth
		self.op = op
		self.args = args
		self.pred = pred
		self.cleanup ()
		self.negation_cleanup()

	def negation_cleanup (self):
		if len(self.args) != 1 or self.op is not None or self.args[0].op is not None:
			return
		arg = self.args[0]
		self.truth = (self.truth == arg.truth)
		self.args = arg.args
		self.pred = arg.pred

	def cleanup (self):
		if self.op == 'imply':
			return
		need_cleanup = True
		for arg in self.args:
			if arg.op is not None and arg.op != self.op:
				need_cleanup = False
		if need_cleanup:
			new_args = []
			for arg in self.args:
				if arg.op is None:
					new_args.append (arg)
				else:
					new_args += arg.args
			self.args = new_args

	def simplify (self):
		if self.op == 'imply':
			if len(self.args) != 2:
				raise Exception (
					"Number of operands not equal to 2 for implication"
				)
			self.op = 'or'
			self.args[0].truth =  not self.args[0].truth
		
		if not self.truth:
			if self.op == 'and':
				self.truth = True
				self.op = 'or'
			elif self.op == 'or':
				self.truth = True
				self.op = 'and'
			for arg in self.args:
				arg.truth = not arg.truth

		for arg in self.args:
			arg.simplify ()

		self.merge ()
		self.cleanup ()
		self.negation_cleanup ()

	def merge (self):
		if self.op  != 'or':
			return
		need_merge = False
		merge_terms = []
		for arg in self.args:
			if arg.op == 'and':
				need_merge = True
				merge_terms.append (arg.args)
			else:
				merge_terms.append ([arg])

		if need_merge:
			self.op = 'and'
			self.args = []
			for arg in product (merge_terms):
				self.args.append (term(op='or', args=list(arg)))

		else:
			self.args = []
			for terms in merge_terms:
				if type(terms) == type([]):
					self.args += terms
				else:
					self.args.append (terms)

	def show (self, c=0):
		print ' '*c, "Truth: ", self.truth
		print ' '*c, "Operator: ", self.op
		for arg in self.args:
			arg.show (c=c+4)
		print ' '*c, "Predicate: ", self.pred

	def get_cnf (self):
		cnf = []
		if self.op != 'and':
			cnf.append(self)
			return cnf
		for arg in self.args:
			cnf = cnf.append (arg)
		return cnf

if __name__ == '__main__':
	x = term (pred='x')
	y = term (pred='y')
	p = term (pred='p')
	q = term (pred='q')
	l = term (op='and', args=[x, y])
	r = term (op='imply', args=[p, q])
	t = term (op='or', args=[l, r])
	#t.show ()
	t.simplify ()
	#t.show ()

	cnf = t.get_cnf ()
	for x in cnf:
		x.show ()
		print "*****"
