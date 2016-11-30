from kb import get_indexed_kb, indexed_kb
from resolver import resolve
import copy

if __name__ == '__main__':
	with open("input.txt", "r") as f:
		raw_data = f.readlines ()
	raw_data = [x.rstrip() for x in raw_data]
	number_of_queries = int(raw_data[0])
	queries = raw_data[1:number_of_queries+1]
	number_of_data = int(raw_data[number_of_queries+1])
	data = raw_data[number_of_queries+2:number_of_queries+2+number_of_data]
	kb = get_indexed_kb (data)
	answers = []
	for query in queries:
		if query[0] == '~':
			query = '(' + query + ')'
		answers.append(resolve (query, copy.deepcopy(kb)))
	with open("output.txt", "w") as f:
		for ans in answers:
			f.write (str(ans) + '\n')
