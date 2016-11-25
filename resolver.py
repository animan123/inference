from kb import indexed_kb
from input import get_cnf
from unify import unify
from utils import isVariable
import copy

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

def resolve (query, kb):
	tbu = indexed_kb ()
	query = cleanup_query (query)
	query[0]["truth"] = not query[0]["truth"]
	tbu.add (query, occur_check=True)

	while not tbu.empty ():
		x = tbu.pop ()
		#print "Popped: ", x
		for x_pred in x:
			if not x_pred["truth"]:
				indices = get_indices (kb.true, x_pred["name"])
			else:
				indices = get_indices (kb.false, x_pred["name"])
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
						#print "x: ", x
						#print "y: ", y
						#print "sub: ", sub
						#print "Resolved: ", resolved_sentence
						tbu.add (resolved_sentence, occur_check=True, verbose=False)
						#print '\n'
		kb.add (x, occur_check=True)
	return False
