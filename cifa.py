import os
import traceback
class synax_error(Exception):
	def __init__(self,msg):
		self.msg=msg
	def __str__(self):
		return '#####error:  '+self.msg+'#######'
if_turial=False

def read_synclib(lib):
	sync_dic={}
	f=open(lib,'r')
	for i in f:
		j=i.strip()
		#print j
		k=j.split(' ')
		#print k,len(k[0])
		if not k[0]:
			break
		sync_dic[k[0]]=k[-1]
	return sync_dic

def find(line,word_buf,sync_dic,target_file,typ = None,):
	if not typ:
		if sync_dic.has_key(word_buf):
			target_file.write(sync_dic[word_buf]+'\n')
		else:
			raise synax_error(line)

	if typ=='id':
		if sync_dic.has_key(word_buf):
			target_file.write(sync_dic[word_buf]+'\n')
		else:
			target_file.write(sync_dic['id']+'   '+word_buf+'\n')
	if typ=='digit':
		target_file.write(sync_dic['digit']+'   '+word_buf+'\n')

	if typ=='string':
		target_file.write(sync_dic['string']+'   '+word_buf+'\n')

def deal_line(line,sync_dic,ff):
	global if_turial
	if if_turial==True:
		if line.endswith('*/'):
			if_turial=False
			return
		else:
			return
	if line.startswith('#') or line.startswith('//') :
		return 

	if line.startswith('/*'):
		if_turial=True
		return
	# deal line
	l=0
	r=0
	#word_buf=''
	while(r<len(line)):
		word_buf=''
		if line[r]==' ' or line[r]=='\t' :
			r=r+1
			l=r
		elif line[r].isalpha():
			r=r+1
			while r<len(line) and (line[r].isalnum() or line[r] == '_'):
				r=r+1
			word_buf=line[l:r]
			find(line,word_buf,sync_dic,typ= 'id',target_file=ff)
			print word_buf
			l=r
		elif line[r].isdigit():
			r=r+1
			while r<len(line) and line[r].isdigit():
				r=r+1
			word_buf=line[l:r]
			l=r
			find(line,word_buf,sync_dic,typ= 'digit',target_file=ff)
			print word_buf
		elif line[r]==',' or line[r]==';' :
			r=r+1
			word_buf=line[l:r]
			l=r
			find(line,word_buf,sync_dic,target_file=ff)
			print word_buf
		elif line[r]== '{' or line[r] =='[' or line[r] == '(':
			r=r+1
			word_buf=line[l:r]
			l=r
			find(line,word_buf,sync_dic,target_file=ff)
			print word_buf

		elif line[r]== '}' or line[r] ==']' or line[r] == ')':
			r=r+1
			word_buf=line[l:r]
			l=r
			find(line,word_buf,sync_dic,target_file=ff)
			print word_buf

		elif line[r]== '*' or line[r] =='/' :
			r=r+1
			word_buf=line[l:r]
			l=r
			find(line,word_buf,sync_dic,target_file=ff)
			print word_buf

		# ++ and -- and + and -
		elif line[r]=='+' or line[r]=='-'  :
			r=r+1
			if r<len(line) and line[r]==line[r-1]:
				r=r+1
			word_buf=line[l:r]
			l=r
			find(line,word_buf,sync_dic,target_file=ff)
			print word_buf

		# < and > and = and ! and <= and >= and == and != 

		elif line[r] =='<' or line[r]=='>' or line[r] =='=' or line[r] =='!':
			r=r+1
			if r<len(line) and line[r]=='=':
				r=r+1
			word_buf=line[l:r]
			l=r 
			find(line,word_buf,sync_dic,target_file=ff)
			print word_buf


		elif line[r] == '&' or line[r] == '|' :
			r=r+1
			if r<len(line) and line[r] == line[r-1]:
				r=r+1
				word_buf=line[l:r]
				l=r
				find(line,word_buf,sync_dic,target_file=ff)
				print word_buf
			else :
				raise synax_error(line)
		elif line[r] =='"' :
			r=r+1
			while r<len(line) and line[r] != '"':
				r=r+1
			if r==len(line):
				raise synax_error(line)
				return
			word_buf=line[l:r]+'"'
			r=r+1
			l=r
			find(line,word_buf,sync_dic,typ='string',target_file=ff)
			print word_buf
		else:
			raise synax_error(line)


def token_deal(aimfile,lib,target):
	if not os.path.exists(aimfile):
		print 'no aimfile'
		return False
	if not os.path.exists(lib):
		print 'no synclib'
		return False
	# read sync lib
	sync_dic=read_synclib(lib)
	
	f=open(aimfile,'r')
	code_buf=[]
	for i in f:
		j=i.strip()
		if not j:
			continue
		code_buf.append(j)
	target_file=open(target,'w')

	for line in code_buf:
		try:
			#print '*'*40
			#target_file.write('*'*40+'\n')
			deal_line(line,sync_dic,target_file)
			#target_file.write('*'*40+'\n')
			#print '*' * 40
 		except synax_error,e:
			print e
	return True
	
if __name__ == '__main__':

	token_deal('test.c','synclib.txt','output.txt')


