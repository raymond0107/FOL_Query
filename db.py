from helper import *
import ply.yacc as yacc
import ly
import copy
import time

class FolKB:
	def __init__(self, clauses = []):
		self.postive = {}
		self.negative = {}
		self.clauses = clauses 
		for clause in clauses:
			self.tell(clause)

	def tell(self, clause):
		for predicate in clause.clause:
			if predicate.flag:
				if predicate.name in self.postive:
					self.postive[predicate.name].append(clause)
				else:
					self.postive[predicate.name] = [clause]
			else:
				if predicate.name in self.negative:
					self.negative[predicate. name].append(clause)
				else:
					self.negative[predicate.name] = [clause]

	def get_match_clause(self, predicate):
		name = predicate.name
		flag = predicate.flag
		mp = None
		if not flag:
			mp = self.postive
		else:
			mp = self.negative
		if name in mp:
			return mp[name]
		else:
			return None

	def get_match_predicate(self, this_predicate, clause):
		for predicate in clause.clause:
			if predicate.name == this_predicate.name and this_predicate.flag != predicate.flag and len(predicate.var) == len(this_predicate.var):
				return predicate
		return None

	def resolution_helper(self, res, this_predicate, this_clause, s):
		for predicate in this_clause.clause:
			if predicate != this_predicate:
				new_vars = []
				for var in predicate.var:
					new_var = var
					while new_var in s:
						new_var = s[new_var]
					new_vars.append(new_var)
				new_predicate = Predicate(predicate.name, new_vars, predicate.flag)
				res.append(new_predicate)

	def resolution(self, query):
		res = []
		flag = False
		for this_predicate in query.clause:
			match_clause_list = self.get_match_clause(this_predicate)
			if not match_clause_list:
				continue
			for that_clause in match_clause_list:
				that_predicate = self.get_match_predicate(this_predicate, that_clause)
				that_var_list = []
				this_var_list = this_predicate.var
				if that_predicate != None:
					that_var_list = that_predicate.var
				else:
					continue
				s = self.unify(this_var_list, that_var_list, {})
				if s == None:
					continue
				else:
					flag = True
					result = []
					self.resolution_helper(result, this_predicate, query, s)
		        	self.resolution_helper(result, that_predicate, that_clause, s)
		        	if len(result) == 0:
		        		return [], flag
		        	else:
		        		new_res = []
		        		not_duplicate = set()
		        		for predicate in result:
		        			not_duplicate.add(predicate)
		        		for predicate in not_duplicate:
		        			new_res.append(predicate)
		        		res.append(Clause(new_res))	
		if not flag:
			return [query],flag
		return res, flag

	def ask(self, query_line):
		p = yacc.parse(query_line).conjunction
		query_raw = p[0].clause[0]
		if (query_raw.flag and (not query_raw.name in self.postive)) or  (not query_raw.flag and (not query_raw.name in self.postive)):
			return False
		visited, queue = set(), [Clause([Predicate(query_raw.name, query_raw.var, not query_raw.flag)])]
		visited.add(Clause([Predicate(query_raw.name, query_raw.var, not query_raw.flag)]))
		l = []
		start = time.time()
		while len(queue) != 0:
			query = queue.pop(0)
			res, flag = self.resolution(query)
			if flag and len(res) == 0:
				return "TRUE"
			for clause in res:
				if not clause in visited:
					self.tell(clause)
					queue.append(clause)
					visited.add(clause)
					l.append(clause)
			now = time.time()
			interval = int(now - start)
			if interval > 23:
				break;
		return "FALSE"

	def is_var(self, arg):
		return arg[0].islower()

	def unify_var(self, var, x, s):
		if var in s:
			return self.unify(s[var], x, s)
		elif self.occur_check(var, x, s):
			return None
		else:
			s[var] = x
			return s

	def unify(self, l, r, s = {}):
		if s == None:
			return None
		if type(l) == type(r) and type(l) == type([]):
			if not l:
				return s
			return self.unify(l[1:], r[1:], self.unify(l[0], r[0], s))
		elif l == r:
			return s
		elif self.is_var(l):
			return self.unify_var(l, r, s)
		elif self.is_var(r):
			return self.unify_var(r, l, s)
		else:
			return None

	def occur_check(self, var, x, s):
		if var == x:
			return True
		elif self.is_var(x) and x in s:
			return self.occur_check(var, s[x], s)
		else:
			return False
