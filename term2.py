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
		if self.op is None and len(self.args) > 1:
			raise Exception ("None operator got more than 1 child")

	def imply_simplify (self):
		for arg in self.args:
			arg.imply_simplify ()
		if self.op == 'imply':
			if len(self.args) != 2:
				raise Exception ("More than 2 operands for imply")
			self.op = 'or'
			self.args[0].truth = not self.args[0].truth

	def negation_simplify (self):
		if not self.truth:
			self.truth = not self.truth
			if self.op == 'or':
				self.op = 'and'
				for arg in self.args:
					arg.truth = not arg.truth
			elif self.op == 'and':
				self.op = 'or'
				for arg in self.args:
					arg.truth = not arg.truth
			elif self.op is None:
				if not len(self.args):
					if self.pred is None:
						raise Exception ("None operator has no predicate and no args")
					self.truth = not self.truth
				else:
					self.args[0].truth = not self.args[0].truth
		for arg in self.args:
			arg.negation_simplify ()

	def and_simplify (self):
		for arg in self.args:
			arg.and_simplify ()
		new_args = []
		if self.op == 'and':
			for arg in self.args:
				if arg.op == 'and':
					new_args = new_args + arg.args
				else:
					new_args = new_args + [arg]
			self.args = new_args

	def or_simplify (self):
		for arg in self.args:
			arg.or_simplify ()
		new_args = []
		if self.op == 'or':
			for arg in self.args:
				if arg.op == 'or':
					new_args = new_args + arg.args
				else:
					new_args = new_args + [arg]
			self.args = new_args

	def just_simplify (self):
		for arg in self.args:
			arg.just_simplify ()
		if self.op is None:
			if len(self.args) > 1:
				raise Exception ("None has more than 1 child after simplify")
			if len(self.args):
				arg = self.args[0]
				self.truth = arg.truth
				self.op = arg.op
				self.pred = arg.pred
				self.args = arg.args

	def merge_simplify (self):
		for arg in self.args:
			arg.merge_simplify ()
		self.merge ()

	def simplify (self):
		#x = input ()
		self.imply_simplify ()
		#self.show ()
		#x = input()
		self.negation_simplify ()
		#self.show ()
		#x = input()
		self.and_simplify ()
		#self.show ()
		#x = input()
		self.or_simplify ()
		#self.show ()
		#x = input()
		self.just_simplify ()
		#self.show ()
		#x = input()
		self.merge_simplify ()

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

	def _get_pred (self, x):
		ret = x.pred
		ret.update ({"truth": x.truth})
		return ret

	def _get_preds (self, x):
		if x.op is None:
			return [self._get_pred(x)]
		elif x.op == 'or':
			return [self._get_pred(y) for y in x.args]
		else:
			raise Exception ("Resolved clause is neither or op nor None op nor and")

	def get_cnf (self):
		cnf = []
		if self.op != 'and':
			cnf.append(self._get_preds(self))
			return cnf
		for arg in self.args:
			cnf.append (self._get_preds(arg))
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
