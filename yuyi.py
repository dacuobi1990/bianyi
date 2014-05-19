import StringIO
class tpe(object):
	def __init__(self):
		self.t=-1
		self.wid=-1

class idval(object):
	def __init__(self):
		self.namelst=[]
		self.off=None
		self.code=[]

class vallist(object):
	def __init__(self):
		self.val=[]


class v(object):
	def __init__(self):
		self.addr = None
		self.code =[]

class f(object):
	def __init__(self):
		self.addr = None
		self.code =[]

class t(object):
	def __init__(self):
		self.addr = None
		self.code=[]

class e(object):
	def __init__(self):
		self.addr = None
		self.code=[]

class ass(object):
	def __init__(self):
		self.code = []

class exc(object):
	def __init__(self):
		self.code=[]
		self.label = None
		self.is_control = False

class bol(object):
	def __init__(self):
		self.v1=None
		self.v2 = None
		self.op = None
	


def read_in(o):
	digit_queue=[]
	id_queue=[]
	string_queue=[]
	for l in o:
		l=l.strip()
		l=l.split(' ')
		if l[0] == '31':
			digit_queue.append(int(l[-1]))

		if l[0] == '33':
			id_queue.append(l[-1])

		if l[0] == '32':
			#print l
			lft=1
			while l[lft] == ' ':
				lft+=1

			content=' '.join(l[lft:])
			string_queue.append(content)


	return digit_queue,id_queue,string_queue

def newtemp(t_index):
	return 't'+str(t_index)

def gen_id_queue(id_queue,st):
	p=0
	for n in st:
		n=n.strip()
		n=int(n)
		if n == 23 or n ==24:
			p=p+1
			if n == 24:
				tmp = id_queue[p]
				id_queue[p] = id_queue[p-1]
				id_queue[p-1] = tmp
	st.close()
	return id_queue[:]

def translate(digit_queue,id_queue,string_queue,st):
	sym_table={}
	offset=0
	declare_set=[]
	exc_set=[]
	tbuf=[]
	vbuf=[]
	fbuf=[]
	ebuf=[]
	boolbuf = []
	assbuf=[]
	last_n=-1
	p=-1

	t_index =0
	l_index =0
	


	#print id_queue
	for n in st:
		n=n.strip()
		n=int(n)
		#print '----------------------'
		#print n
		if n == 19: # ['type', 'int']
			tt=tpe()
			tt.t='int'
			tt.wid=4
			declare_set.append(tt)
		elif n== 23: #['idval', 'id']
			idl=idval()
			idl.namelst.append(id_queue.pop(0))
			#print 'id',idl.namelst
			declare_set.append(idl)

		elif n==22:  #['idval', 'idval', ',', 'idval']
			idl1=declare_set.pop()
			idl2=declare_set.pop()
			idl = idval()
			idl.namelst=idl2.namelst+idl1.namelst
			declare_set.append(idl)

		elif n == 12:#fill in the sym_table
			tt=declare_set[0]
			idl = declare_set[1]
			for i in idl.namelst:
				sym_table[i]=[tt.t,offset]
				offset+=tt.wid

			declare_set=[]

			#ec = exc()
			#ec.label = 'L'+str(l_index)
			#l_index += 1
			#exc_set.append(ec)
		elif n == 21:#['vallist', 'digit']
			if last_n == 19:
				digit_queue.pop(0)
			vl = vallist()
			vl.val.append(digit_queue.pop(0))
			declare_set.append(vl)


		elif n == 20: # ['vallist', 'vallist', ',', 'vallist']
			vl1 = declare_set.pop()
			vl2 = declare_set.pop()
			vl = vallist()
			vl.val = vl2.val + vl1.val
			declare_set.append(vl)

		elif n == 11: # 'exc', 'type', 'id', '[', 'digit', ']', '=', '{', 'vallist', '}', ';']
			tt=declare_set[0]
			vl= declare_set[1]
			array_id = id_queue.pop(0)
			vlst=vl.val[:]
			sym_table[array_id]=[tt.t+'-array',tt.wid,offset,vlst]
			offset += tt.wid * len(vlst)
			declare_set=[]
			#ec = exc()
			#ec.label = 'L'+str(l_index)
			#l_index += 1
			#exc_set.append(ec)

# -------------------------------------------------------------------------------------ass


		elif n == 0: 
			#(0, ['v', 'idval'])
			vv = v()
			idl = declare_set.pop()
			if not idl.off:
				####
				if not sym_table.has_key(idl.namelst[0]):
					print idl.namelst[0] + 'not declare'
				vv.addr = idl.namelst[0]
				vv.code = vv.code[:] + idl.code[:]
			else:
				vv.addr = newtemp(t_index)
				#print 'vv.addr',vv.addr
				t_index+=1
				vv.code = vv.code[:] + idl.code[:]
				####
				if not sym_table.has_key(idl.namelst[0]):
					print idl.namelst[0] + 'not declare'
					return
				wid = sym_table[idl.namelst[0]][1]
				cde = vv.addr + '='+idl.namelst[0]+'['+str(wid)+'*' +idl.off+']'
				#print 'cde' , cde
				vv.code.append(cde)

			vbuf.append(vv)

		elif n == 1:
			# ['v', 'digit']
			vv =v()
			vv.addr = str(digit_queue.pop(0))
			vbuf.append(vv)

		elif n == 35:
			#['f', 'v']
			ff = f()
			vv = vbuf.pop()
			ff.addr = vv.addr
			ff.code = vv.code[:]
			fbuf.append(ff)

		elif n == 34:
			# ['f', '(', 'e', ')']
			ff = f()
			ee = ebuf.pop()
			ff.addr = ee.addr
			ff.code = ee.code[:]
			fbuf.append(ff)

		elif n == 33:
			#['t', 'f']
			tt = t()
			ff = fbuf.pop()
			tt.addr = ff.addr
			tt.code = ff.code[:]
			tbuf.append(tt)

		elif n == 32:
			#['t', 't', '/', 'f']
			tt = tbuf.pop()
			ff = fbuf.pop()
			ad = newtemp(t_index)
			t_index+=1
			cde = ad +'='+tt.addr +'/'+str(ff.addr)
			tt.addr = ad
			tt.code = tt.code [:]+ff.code[:] 
			tt.code.append(cde)
			tbuf.append(tt)

		elif n == 31:
			#['t', 't', '*', 'f']
			tt = tbuf.pop()
			ff = fbuf.pop()
			ad = newtemp(t_index)
			t_index+=1
			cde = ad +'='+tt.addr +'*'+str(ff.addr)
			tt.addr = ad 
			tt.code = tt.code [:]+ff.code[:] 
			tt.code.append(cde)
			tbuf.append(tt)

		elif n == 30:
			# ['e', 't']
			ee=e()
			tt = tbuf.pop()
			ee.addr = tt.addr
			ee.code = tt.code[:]
			ebuf.append(ee)

		elif n == 29:
			#['e', 'e', '-', 't']
			ee = ebuf.pop()
			tt = tbuf.pop()
			ad = newtemp(t_index)
			t_index+=1
			cde =ad + '='+ ee.addr +'-'+ str(tt.addr)
			ee.addr = ad 
			ee.code = ee.code [:]+tt.code[:] 
			ee.code.append(cde)
			ebuf.append(ee)

		elif n == 28:
			# ['e', 'e', '+', 't']
			ee = ebuf.pop()
			tt = tbuf.pop()
			ad = newtemp(t_index)
			t_index+=1
			cde = ad + '='+ ee.addr +'+'+ str(tt.addr)
			ee.addr = ad 
			ee.code = ee.code [:]+tt.code[:] 
			ee.code.append(cde)
			ebuf.append(ee)



		elif n == 25:
			#['ass', 'idval', '=', 'e']
			a = ass()
			ee=ebuf.pop()
			a.code=ee.code[:]
			idl = declare_set.pop()
			addr = idl.namelst[0]
			if not sym_table.has_key(addr):
				print addr + ' not declare'
			cde = addr + '=' +str(ee.addr)
			a.code.append(cde)
			assbuf.append(a)


		elif n == 26 :
			# ['ass', 'idval', '++']
			a=ass()

			idl = declare_set.pop()
			if not idl.off:
				addr = idl.namelst[0]
				cde = addr + '='+addr +'+1'
				a.code.append(cde) 
			else:
				addr = newtemp(t_index)
				t_index+=1
				cde = addr + '='+idl.namelst[0]+'['+idl.off+']'
				a.code.append(cde)
				cde = addr + '='+addr +'+1'
				a.code.append(cde)

			assbuf.append(a)


		elif n == 27:
			#  ['ass', 'idval', '--']
			a=ass()

			idl = declare_set.pop()
			if not idl.off:
				addr = idl.namelst[0]
				cde = addr + '='+addr +'-1'
				a.code.append(cde) 
			else:
				addr = newtemp(t_index)
				t_index+=1
				cde = addr + '='+idl.namelst[0]+'['+idl.off+']'
				a.code.append(cde)
				cde = addr + '='+addr +'-1'
				a.code.append(cde)

			assbuf.append(a)


		elif n == 13:
			# ['exc', 'ass', ';']
			declare_set = []
			tbuf =[]
			ebuf =[]
			fbuf=[]
			vbuf = []
			a=assbuf.pop()
			ec = exc()
			ec.label = 'L'+str(l_index)
			l_index += 1

			ec.code = a.code[:]
			exc_set.append(ec)




		elif n == 24:
			#['idval', 'idval', '[', 'e', ']']
			idl = idval()
			idl1 = declare_set.pop()
			tp = idl1.namelst[0]
			idl.namelst.append(tp)
			ee = ebuf.pop()
			idl.off = ee.addr
			idl.code = idl.code[:] + ee.code[:]
			declare_set.append(idl)

		elif n == 17:
			#['exc', 'return', 'e', ';']

			ee  = ebuf.pop()
			cde = 'ret ' + ee.addr
			ec = exc()
			ec.label = 'L'+str(l_index)
			l_index += 1
			ec.code.append(cde)
			exc_set.append(ec)

		elif n == 2:
			# ['bool', 'v', '>=', 'v']
			bb = bol()
			v2 = vbuf.pop()
			v1 = vbuf.pop()
			op = '>='
			bb.v1=v1
			bb.v2=v2
			bb.op = op
			boolbuf.append(bb)


		elif n == 3:
			# ['bool', 'v', '<=', 'v']
			bb = bol()
			v2 = vbuf.pop()
			v1 = vbuf.pop()
			op = '<='
			bb.v1=v1
			bb.v2=v2
			bb.op = op
			boolbuf.append(bb)


		elif n == 4:
			# ['bool', 'v', '>', 'v']
			bb = bol()
			v2 = vbuf.pop()
			v1 = vbuf.pop()
			op = '>'
			bb.v1=v1
			bb.v2=v2
			bb.op = op
			boolbuf.append(bb)


		elif n == 5:
			# ['bool', 'v', '<', 'v']
			bb = bol()
			v2 = vbuf.pop()
			v1 = vbuf.pop()
			op = '<'
			bb.v1=v1
			bb.v2=v2
			bb.op = op
			boolbuf.append(bb)


		elif n == 6:
			# ['bool', 'v', '==', 'v']
			bb = bol()
			v2 = vbuf.pop()
			v1 = vbuf.pop()
			op = '=='
			bb.v1=v1
			bb.v2=v2
			bb.op = op
			boolbuf.append(bb)


		elif n == 7:
			# ['bool', 'v', '!=', 'v']
			bb = bol()
			v2 = vbuf.pop()
			v1 = vbuf.pop()
			op = '!='
			bb.v1=v1
			bb.v2=v2
			bb.op = op
			boolbuf.append(bb)


		elif n == 10:
			#['exc', 'exc', 'exc']
			#for i in exc_set:
				#print i.label,i.code
			#print
			last1 = exc_set.pop()
			last2 = exc_set.pop()
			if last1.is_control == False and last2.is_control == False:
				last = exc()
				last.label = last2.label
				l_index -= 1
				last.code = last2.code[:] + last1.code[:]
				exc_set.append(last)
			else:
				exc_set.append(last2)
				exc_set.append(last1)

			#for i in exc_set:
				#print i.label,i.code
			#print

		elif n == 16:
			#['exc', 'if', '(', 'bool', ')', '{', 'exc', '}', 'else', '{', 'exc', '}']
			ec2=exc_set.pop()
			ec1=exc_set.pop()
			ec = exc()
			ec.is_control = True
			ec2.is_control = True
			ec1.is_control = True
			ec.label = 'L'+str(l_index)
			l_index += 1
			bl = boolbuf.pop()

			cde = 'if ' + bl.v1.addr + bl.op+bl.v2.addr +' goto ' + ec1.label
			ec.code.append(cde)
			cde = 'goto '+ec2.label
			ec.code.append(cde)
			cde = 'goto'+'if_next'
			ec1.code.append(cde)
			exc_set.append(ec)
			exc_set.append(ec1)
			exc_set.append(ec2)

		elif n == 15:
			#['exc', 'while', '(', 'bool', ')', '{', 'exc', '}']
			ec1 = exc_set.pop()
			ec = exc()
			ec.is_control = True
			ec1.is_control = True
			ec.label = 'L'+str(l_index)
			l_index += 1
			bl = boolbuf.pop()

			cde = 'if ' + bl.v1.addr + bl.op+bl.v2.addr +' goto ' + ec1.label
			ec.code.append(cde)
			cde = 'goto '+'while_next'
			ec.code.append(cde)
			cde = 'goto '+ ec.label
			ec1.code.append(cde)
			exc_set.append(ec)
			exc_set.append(ec1)

		elif n == 14:
			# , ['exc', 'for', '(', 'ass', ';', 'bool', ';', 'ass', ')', '{', 'exc', '}']
			ass2 = assbuf.pop()
			ass1 = assbuf.pop()
			bl = boolbuf.pop()
			ec1 = exc_set.pop()
			ec1.is_control = True
			pre_ec = exc()
			pre_ec.is_control = True
			pre_ec.label = 'L'+str(l_index)
			l_index += 1
			pre_ec.code+= ass1.code[:]

			ec = exc()
			ec.is_control = True
			ec.label = 'L'+str(l_index)
			l_index+=1
			cde = 'if ' + bl.v1.addr + bl.op+bl.v2.addr +' goto ' + ec1.label
			ec.code.append(cde)
			cde = 'goto' + 'fornext'
			ec.code.append(cde)
			ec1.code+=ass2.code[:]
			cde = 'goto '+ ec.label
			ec1.code.append(cde)

			exc_set.append(pre_ec)
			exc_set.append(ec)
			exc_set.append(ec1)


		elif n == 18:
			#['exc', 'printf', '(', 'string', ',', 'idval', ')', ';']
			ec =exc()
			ec.label = 'L'+str(l_index)
			l_index+=1
			addr = newtemp(t_index)
			t_index+=1
			string = string_queue.pop()
			string =StringIO.StringIO(string)
			cde = addr + '='+ string.read()

			ec.code.append(cde)
			cde = 'param =' +addr
			ec.code.append(cde)
			idl = declare_set.pop()
			cde = 'param=' + idl.namelst[0] 
			ec.code.append(cde)
			cde = 'call' + ' printf '+'2'
			ec.code.append(cde)
			exc_set.append(ec)


		elif n == 9: 
			#  ['pro', 'int', 'main', '(', ')', '{', 'exc', '}']
			pass

		elif n == 8:
			#['s', 'pro']
			pass

		else :
			pass

		last_n =n
		#print '----------------------'


	return sym_table,exc_set

def fill(exc_set):
	num =len(exc_set)
	for i in range(num):
		if exc_set[i].code[-1] =='gotofornext':
			next = exc_set[i+2].label
			exc_set[i].code.pop()
			cde = 'goto '+next
			exc_set[i].code.append(cde)

		if exc_set[i].code[-1] =='goto while_next':
			next = exc_set[i+2].label
			exc_set[i].code.pop()
			cde = 'goto '+next
			exc_set[i].code.append(cde)

		if exc_set[i].code[-1] =='gotoif_next':
			next = exc_set[i+2].label
			exc_set[i].code.pop()
			cde = 'goto '+next
			exc_set[i].code.append(cde)


	return exc_set



if __name__ == '__main__':
	o=open('output.txt','r')
	digit_queue,id_queue,string_queue=read_in(o)
	print'digit_queue:', digit_queue
	print 'id_queue:', id_queue
	print 'string_queue:',string_queue

	st=open('yufa_output.txt','r')

	sym_table,exc_set= translate(digit_queue,id_queue,string_queue,st)
	for i in sym_table:
		print i,sym_table[i]

	exc_set=fill(exc_set)

	for i in exc_set:
		print i.label,i.code


	