import operator
def build_table(syn,pra):
	V={}
	T={}
	for i in syn:
		i = i.strip()
		i = i.split(' ')

		if not i[0]:
			break

		T[i[0]] = int(i[-1])
		T['#'] =0

 	#re = sorted(T.iteritems(),key=operator.itemgetter(-1))
 	#for i in re:
 		#print i
 	for i in pra:
 		i = i.strip()
 		i=i.split(' ')

 		if not i[0]:
 			continue

 		V[i[0]] = int(i[-1])

 	#re =sorted(V.iteritems(),key=operator.itemgetter(-1))
 	#for i in re:
 		#print i

 	return T,V

def deal_generate(T,V,wen):
 	gen={}
 	for i in wen:
 		i= i.strip()
 		i=i.split(' ')
 		
 		if not i[0]:
 			continue


 		l=V[i[0]]
 		r=i[2:]

 		rr=[]
 		for j in r:
 			if j in V:
 				rr.append('V'+str(V[j]))

 			elif j in T:
 				rr.append('T'+str(T[j]))

 		l='V'+str(l)

 		if not gen.has_key(l):
 			gen[l] = []

 		gen[l].append(rr)


 	return gen

def first(x,gen):
 	fst=set([])
 	if  x[0] =='T':
 		fst.add(x)

 	elif x[0] == 'V':
 		for i in gen[x]:
 			if i[0] [0] =='T':
 				fst.add(i[0])

 			if i[0][0] == 'V' and i[0] != x:
 				fst=fst|first(i[0],gen)
 				#print '!!!!',fst


 	else:
 		print 'wrong'

 	return fst


def  calc_ba(aBb,Bp,a):
	if Bp == len(aBb)-1:
		ba =[a]

	else:
		ba=aBb[Bp+1:]
		ba.append(a)

	return ba


def in_c(l,c):
	for ll in c:
		if l[0] == ll[0] and l[2] ==ll[2] and ''.join(l[1]) ==''.join(ll[1]):
			return True

	return False






def closure(I,gen):
 	c=I[:]
 	num =len(c)
 	while 1:
 		for l in c:
 			aBb=l[1][:]
 			p=aBb.index('.')
 			if p == len(aBb)-1:
 				continue

 			B=aBb[p+1]
 			if B[0] == 'V':
 				#print  '!', gen[B]
 				ba =calc_ba(aBb,p+1,l[2]) 
 				nb=first(ba[0],gen)
 				for g in gen[B]:
 					for b in nb:
 						nl=[B,['.']+g,b]
 						if not in_c(nl,c):
 							c.append(nl)
 		if len(c) == num:
 			break


 		num = len(c)

 	return c

def read_clo(I,T,V):
	if not I:
		print 'null'
		return 

	for i in I:
		if type(i) == type('f'):
			print i
			break
		l=i[0]
		r=i[1]
		n=i[2]
		#print l,r,n
		for i in V:
			if V[i] ==int(l[1:]):
				l=i
				break

		rr=[]
		for j in r:
			if  j == '.':
				rr.append(j)

			if j[0] == 'V':
				for i in V:
					if V[i] == int(j[1:]):
						rr.append(i)
						break

			if j[0] == 'T':
				for i in T:
					if T[i] == int(j[1:]):
						rr.append(i)
						break

		for i in T:
			if T[i] ==int(n[1:]):
				n=i
				break


		print l,rr,n


def  go(I,x,gen):
	j=[]
	for i in I:
		l=i[0]
		r=i[1][:]
		b=i[2]
		p=r.index('.')
		if p !=len(r)-1:
			if r[p+1]==x:
				del r[p]
				r.insert(p+1,'.')
				j.append([l,r,b])
				

	return closure(j,gen)


def is_equal(re,c):
	for l in re:
		if not in_c(l,c):
			return False

	if len(re) != len(c):
		return False

	return True


def go_in_cc(re,cc):
	for k in cc:
		c=cc[k]
		if is_equal(re,c):
			#print '!!!!',k
			return True,k

	return False,-1


def fill_table(x,k,index,action,goto):
	if x[0] == 'T':
		p=int(x[1:])
		action[k][p]='s'+str(index)

	elif x[0] =='V':
		p=int(x[1:])
		#print old_num,'v'+str(p),index
		goto[k][p] = str(index)

	else :
		print 'wrong 1'


def st_gen(gen):
	st=[]
	for i in gen:
		l=i
		for j in gen[i]:
			#print l,j
			g=[]
			g.append(l)
			g=g+j[:]
			st.append(g)

	return st

def g_equal(g,gg):
	if len(g) !=len(gg):
		return False
	else:
		n=len(g)
		for i in range(n):
			if g[i] != gg[i]:
				return False

	return True

def find(g,st):
	for p,gg in enumerate(st):
		if g_equal(g,gg) ==True:
			return p

	return -1



def fill_table_1(k,cc,st,action,I):
	start=I[0]
	ll=start[0]
	rr=start[1][1:]
	bb=start[2]
	c=cc[k]
	#print '---------------'
	
	for i in c:
		#print '!!!',i
		l=i[0]
		r=i[1]
		b=i[2]
		if r.index('.') == len(r)-1:
			r=r[0:len(r)-1]
			#print l,r,b
			if l==ll and len(r) ==1 and r[0] ==rr[0] and b == bb:
				action[k][0] ='acc' # #-->T0

			else:
				g=[]
				g.append(l)
				g=g+r
				j=find(g,st)
				if j == -1:
					print 'wrong 2'
				p=int(b[1:])
				action[k][p]='r'+str(j)





	#print '--------------'



def clo_set(I,gen,T,V):

	action={}
	goto={}
	st=st_gen(gen)

	tv=[]
	for i in T:
		tv.append('T'+str(T[i]))

	for i in V:
		tv.append('V'+str(V[i]))

	cc={}
	num=0
	p=num
	cc[num]=closure(I,gen)

	t=0
	while 1:
		for k in cc.keys():
			
			II = cc[k]
			if action.has_key(k) and goto.has_key(k):
				continue
			print k
			if not action.has_key(k):
				action[k]=['-']*len(T)
			if not goto.has_key(k):
				goto[k]=['-']*len(V)

			fill_table_1(k,cc,st,action,I)
			for x in tv:
				re = go(II,x,gen)
				if re :
					flag,index=go_in_cc(re,cc)
					if flag:
						#pass
						fill_table(x,k,index,action,goto)
						

					else:
						
						num=num+1
						cc[num]=re
						fill_table(x,k,num,action,goto)

		if p == num:
			break

		p=num
		t=t+1

	return cc,action,goto,st

def deal_input(f):
	buf=[]
	for l in f:
		l=l.strip()
		l=l.split(' ')
		if not l[0]:
			continue

		ele='T'+str(l[0])

		buf.append(ele)

	buf.append('T0')


	return buf


def lr(buf,action,goto,st):
	yufa_out=[]
	sta_stk=[0]
	pre_stk=['T0']
	p=0
	t=0
	while 1:
		s=sta_stk[-1]
		a=buf[p]
		try:
			aa=int(a[1:])
		except:
			print a,type(a[1:])
			raise ValueError
		aa=int(a[1:])
		rslt=action[s][aa]
		
		if rslt[0]=='s':
			i=int(rslt[1:])
			pre_stk.append(a)
			sta_stk.append(i)
			p=p+1

		elif rslt[0] =='r':
			k=int(rslt[1:])
			g=st[k]
			A=g[0]
			AA=int(A[1:])
			b=len(g[1:])
			for i in range(0,b):
				pre_stk.pop()
				sta_stk.pop()

			s1=sta_stk[-1]
			try:
				ns=goto[s1][AA]
			except:
				print s1,AA
				raise IndexError

			ns=goto[s1][AA]
			ns=int(ns)
			pre_stk.append(A)
			sta_stk.append(ns)
			yufa_out.append(k)

		elif rslt == 'acc':
			return yufa_out

		else:
			print rslt,s,a,aa
			print 'wrong'
			return yufa_out
			#return None



def read(num,g,T,V):
	gg=[]
	for i in g:
		n=i[1:]
		if i[0] =='T':
			for k in T:
				if str(T[k]) == n:
					gg.append(k)

		if i[0] =='V':
			for k in V:
				if str(V[k]) == n:
					gg.append(k)

	return num,gg

#test_action={0:['-','s3','s4'],1:['acc','-','-'],2:['-','s3','s4'],3:['-','s3','s4'],4:['r3','r3','r3'],5:['r1','r1','r1'],6:['r2','r2','r2']}
#test_goto={0:['1','2'],1:['-','-'],2:['-','5'],3:['-','6'],4:['-','-'],5:['-','-'],6:['-','-']}
#test_st=[['V0','V0'],['V0','V1','V1'],['v1','T1','V1'],['V1','T2']]
#buf=['T2','T1','T2','T0']
#yufa_out=lr(buf,test_action,test_goto,test_st)
#print yufa_out


if __name__ == '__main__':
	syn = open('synclib.txt','r')
	pra = open('pragval.txt','r')
	T,V=build_table(syn,pra)
	wen =open('wenfa.txt','r')
	gen=deal_generate(T,V,wen)

	test={'V0':[['V1']],
	               'V1':[['V2','T1','V3'],['V3']],
	               'V2':[['T2','V3'],['T3']],
	               'V3':[['V2']] }

	TT={'#':0,'=':1,'*':2,'i':3}
	VV={'s1':0,'s':1,'L':2,'R':3}

	I=[['V0',['.','V1'],'T0']]
	

        r,action,goto,st=clo_set(I,gen,T,V)

        print '--------------------------------------'
        print 'action'
        for i in action:
        	print i,action[i]

        print '--------------------------------------'
        print 'goto'
        for i in goto:
        	print i,goto[i]
        print '--------------------------------------'
        print 'st'
        for j,i in enumerate(st):
        	print read(j,i,T,V)
        print '--------------------------------------'
        #for k in r:
        	#print k
        	#print r[k]
        	#read_clo(r[k],TT,VV)


        

        
        f=open('output.txt','r')
        buf=deal_input(f)
        yufa_out=lr(buf,action,goto,st)
        f.close()

        for i in yufa_out:
        	print  read(i,st[i],T,V)
        	#print i,st[i]

        f=open('yufa_output.txt','w')
        for i in yufa_out:
        	f.write(str(i)+'\n')


     




       








