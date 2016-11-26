from kb import get_indexed_kb, indexed_kb
from resolver import resolve
import copy

if __name__ == '__main__':
	with open("input2", "r") as f:
		raw_data = f.readlines ()
	raw_data = [x.rstrip() for x in raw_data]
	number_of_queries = int(raw_data[0])
	queries = raw_data[1:number_of_queries+1]
	data = raw_data[number_of_queries+2:]
	kb = get_indexed_kb (data)
	
	for query in queries:
		print resolve (query, copy.deepcopy(kb))
