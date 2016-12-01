from kb import indexed_kb
from input import get_cnf
from unify import unify
from utils import isVariable, standardize, hasConstants
import copy
import time

def isTrue (resolved_sentence):
	if len(resolved_sentence) != 2:
		return False
	a = resolved_sentence[0]
	b = resolved_sentence[1]
	if a["name"] == b["name"] and a["args"] == b["args"] and a["truth"] != b["truth"]:
		return True
	return False

def get_resolved_sentence (x, y, x_pred, y_pred, sub):
	x = [xx for xx in x if xx != x_pred]
	y = [yy for yy in y if yy != y_pred]
	resolved_sentence = x + y
	for i, pred in enumerate (resolved_sentence):
		for j, arg in enumerate (pred["args"]):
			if isVariable (arg) and arg in sub:
				resolved_sentence[i]["args"][j] = sub[arg]
	return resolved_sentence

def cleanup_query (query):
	return get_cnf (query)[0]

def get_indices (dic, name):
	if name not in dic:
		return []
	return dic[name]

def isRecursive (sentence):
	for x in sentence:
		for y in sentence:
			if x["name"] == y["name"] and x["args"] != y["args"] and x["truth"] != y["truth"]:
				return True
	return False

def sanity_check (parent, kb, threshold):
	for index in parent:
		if parent[index] > threshold and isRecursive (kb.all[index]):
			return False
	return True

def resolve (query, kb):
	threshold = kb.size
	tbu = indexed_kb ()
	query = cleanup_query (query)
	query[0]["truth"] = not query[0]["truth"]
	tbu.add (query, occur_check=True)
	iter = 0
	#print query
	start = time.time ()
	while not tbu.empty ():
		iter += 1
		x, parent = tbu.pop ()
		if not sanity_check (parent, kb, threshold):
			continue
		#print "Popped: ", x
		for x_pred in x:
			if not x_pred["truth"]:
				indices = get_indices (kb.true, x_pred["name"])
			else:
				indices = get_indices (kb.false, x_pred["name"])
			#print "X_pred is ", x_pred, indices
			for index in indices:
				y = kb.all [index]
				for y_pred in y:
					sub = unify (x_pred, y_pred)
					if sub is not None:
						resolved_sentence = get_resolved_sentence (
							copy.deepcopy(x),
							copy.deepcopy(y),
							copy.deepcopy(x_pred),
							copy.deepcopy(y_pred),
							sub
						)
						if resolved_sentence == []:
							return True
						if isTrue (resolved_sentence):
							return False
						resolved_sentence = standardize (resolved_sentence)
						new_parent = copy.deepcopy (parent)
						if index not in new_parent:
							new_parent[index] = 0
						new_parent[index] += 1
						tbu.add (resolved_sentence, new_parent, occur_check=True, verbose=False)
						print tbu.size, iter
						if len(resolved_sentence) > 10000:
							print "x: ", x
							print "y: ", y
							print "sub: ", sub
							print "Resolved: ", resolved_sentence
							print tbu.size
							print '\n'
							xxx = input ()
		end = time.time ()
		if (end - start) > 10:
			print "Breaking out in 10 seconds"
			break
		x = standardize (x)
		kb.add (x, occur_check=True)
	return False
