from input import get_cnf
from utils import isVariable, isConstant
from unify import isSame
import copy

def get_kb (data):
	cnfs = []
	for s in data:
		#print s
		new = get_cnf(s)
		for cnf in new:
			cnfs.append (cnf)
	counter = 0
	for i, t in enumerate (cnfs):
		counter += 1
		for k, child in enumerate (t):
			for j, var in enumerate (child):
				if isVariable (var):
					cnfs[i][k][j] = var + str(counter)
	return cnfs

class indexed_kb:
	def __init__ (self, another=None):
		if another is None:
			self.true = {}
			self.false = {}
			self.all = []
			self.size = 0
			self.current = 0
		else:
			self.true = another.true
			self.false = another.false
			self.all = another.all
			self.size = another.size
			self.current = another.current

	def empty (self):
		return (self.size == 0)

	def pop (self):
		y = self.all [self.current]
		self.current += 1
		self.size -= 1
		return y

	def add_true (self, index, name):
		if name not in self.true:
			self.true[name] = []
		self.true[name].append (index)
		self.true[name] = sorted(self.true[name], key=lambda x: len(self.all[x]))

	def add_false (self, index, name):
		if name not in self.false:
			self.false[name] = []
		self.false[name].append (index)
		self.false[name] = sorted(self.false[name], key=lambda x: len(self.all[x]))

	def match_pred (self, p1, p2):
		if p1["name"] != p2["name"]:
			return False
		for arg1, arg2 in zip (p1["args"], p2["args"]):
			if isVariable (arg1) and isConstant (arg2):
				return False
			if isConstant (arg1) and isVariable (arg2):
				return False
			if isConstant (arg1) and isConstant (arg2) and arg1 != arg2:
				return False
		return True

	def match (self, x, y):
		if len(x) != len(y):
			return False
		for p1, p2 in zip(x, y):
			if not self.match_pred (p1, p2):
				return False
		return True

	def occur_check_pred_truth (self, name, x):
		if name not in self.true:
			return False
		indices = self.true[name]
		ret = True
		for i in indices:
			y = self.all [i]
			if self.match (x, y):
				#print "Self match with", y
				return True
			'''
			if isSame (copy.deepcopy(x), copy.deepcopy(y)):
				#print "Is same match with", y
				return True
			'''
		return False

	def occur_check_pred_false (self, name, x):
		if name not in self.false:
			return False
		indices = self.false[name]
		for i in indices:
			y = self.all [i]
			if self.match (x, y):
				#print "Self match with", y
				return True
			'''
			if isSame (copy.deepcopy(x), copy.deepcopy(y)):
				#print "Isame match with ", y
				return True
			'''
		return False

	def occur_check (self, x):
		for pred in x:
			name = pred["name"]
			truth = pred["truth"]
			if truth:
				if self.occur_check_pred_truth (name, x):
					return True
			else:
				if self.occur_check_pred_false (name, x):
					return True
		return False

	def add (self, x, occur_check=False, verbose=False):
		x = sorted (x, key=lambda x: x["name"])
		if occur_check and self.occur_check (x):
			if verbose:
				print "Not adding"
				for pred in x:
					print pred
				print '\n'
			return
		if verbose:
			print "Adding"
			for pred in x:
				print pred
			print '\n'
		self.all.append (x)
		self.size += 1
		index = len(self.all) - 1
		for pred in x:
			if pred["truth"]:
				self.add_true (index, pred["name"])
			else:
				self.add_false (index, pred["name"])

def get_indexed_kb (data):
	kb = get_kb (data)
	ikb = indexed_kb ()
	for cnf in kb:
		ikb.add (cnf, occur_check=True)
	return ikb
