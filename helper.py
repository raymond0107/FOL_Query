import itertools

class Conjunction:
	def __init__(self, conjunction):
		self.conjunction = conjunction

	def do_or(self, that):
		res = []
		for this_clause in self.conjunction:
			for that_clause in that.conjunction:
				res.append(this_clause.do_or(that_clause))
		return Conjunction(res)

	def do_and(self, that):
		res = []
		for this_clause in self.conjunction:
			res.append(this_clause)
		for that_clause in that.conjunction:
			res.append(that_clause)
		return Conjunction(res)

	def do_not(self):
		data_raw = []
		for clauses in self.conjunction:
			temp = set()
			for predicate in clauses.clause:
				temp.add(predicate)
			data_raw.append(list(temp))
		data_process = []
		for group in itertools.product(*data_raw):
			data_process.append(group)
		res = []
		for clauses in data_process:
			temp = []
			for predicate in clauses:
				temp.append(predicate.do_not())
			res.append(Clause(temp))
		return Conjunction(res)

class Clause:
	def __init__(self, clause):
		self.clause = clause

	def do_or(self, that):
		res = set()
		for this_predicate in self.clause:
			res.add(this_predicate)
		for that_predicate in that.clause:
			res.add(that_predicate)
		return Clause(list(res))
	
	def do_not(self):
		res = []
		for predicate in self.clause:
			res.append([predicate.do_not()])
		return Clause(res)

	def do_and(self, that):
		res = []
		res.append(self)
		res.append(that)
		return Conjunction(res)

	def __hash__(self):
		l = []
		for predicate in self.clause:
			l.append(str(predicate))
		l.sort()
		s = ""
		for predicate in l:
			s += str(predicate)
		return hash(s)
	
	def __eq__(self, that):
		this = Clause(self.clause)
		another = Clause(that.clause)
		for x in this.clause:
			if x in another.clause:
				another.clause.remove(x)
		return len(another.clause) == 0

	def __str__(self):
		s = "["
		flag = False
		for predicate in self.clause:
			s += str(predicate) + "|"
			flag = True
		if flag:
			s = s[:-1]
		s += "]"
		return s

class Predicate:
	def __init__(self, name, var, flag = True):
		self.name = name
		self.var = var
		self.flag = flag

	def do_not(self):
		return Predicate(self.name, self.var, not self.flag)

	def __hash__(self):
		return hash(str(self.name) + str(self.var) + str(self.flag))

	def __eq__(self, that):
		return (str(self.name) + str(self.var) + str(self.flag)) == (str(that.name) + str(that.var) + str(that.flag))

	def __str__(self):
		s = ""
		if self.flag:
			s += self.name + '(' + ', '.join(self.var) + ')'
		else:
			s += '~' + self.name + '(' + ', '.join(self.var) + ')'
		return s