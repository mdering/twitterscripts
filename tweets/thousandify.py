#!/usr/bin/env python

name = "whitehouse"
f = open(name+".txt",'r')
g = open(name+"100.txt",'w')
rows = []
for line in f:
	sline = line.strip()
	rows.append(sline)
	if len(rows) == 100:
		g.write(','.join(rows)+"\n")
		rows=[]

g.write(','.join(rows))
rows=[]
g.close()