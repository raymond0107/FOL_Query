import ply.yacc as yacc
import ly
from db import FolKB
from helper import *
import copy

f = open("input.txt")

query_num = int(f.readline())
query_list = []

for i in range(query_num):
	query_list.append(f.readline())

predicate_num = int(f.readline())
predicate_list = []

for i in range(predicate_num):
	predicate_list.append(f.readline())

p = []
for line in predicate_list:
	p.append(yacc.parse(line).conjunction)

clause_list = []
for clause_array in p:
	for clause in clause_array:
		clause_list.append(clause)

db = FolKB(clause_list)

db_list = []
for i in range(query_num):
	db_list.append(copy.deepcopy(db))

target = open("output.txt", 'w')

for i in range(query_num):
	s = db_list[i].ask(query_list[i])
	print s
	target.write(s)
	target.write("\n")

target.close()