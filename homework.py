if __name__ == '__main__':
	with open("input", "r") as f:
		raw_data = f.readlines ()
	raw_data = [x.rstrip() for x in raw_data]
	number_of_queries = int(raw_data[0])
	queries = raw_data[1:number_of_queries+1]
	data = raw_data[number_of_queries+2:]
	print data