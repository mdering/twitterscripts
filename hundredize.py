#!/usr/bin/env python







def hundredize(filename):
	f = open(filename,'r')
	s=[]
	qs=[]


	for line in f:
		d=line.strip()
		s.append(d)
		if len(s)==100:
			qs.append(','.join(s));
			#print qs
			s=[]

	qs.append(','.join(s))

	f.close()

	g=open("fixed_"+filename,'w')

	for q in qs:
		g.write(q+"\n")
	g.close()


hundredize('sdlinks.csv');
hundredize('links.csv');


exit();