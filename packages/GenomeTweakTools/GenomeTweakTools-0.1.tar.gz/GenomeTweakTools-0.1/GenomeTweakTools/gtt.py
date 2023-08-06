import re

class base():
	def __init__(self, loc):
		self.value=loc
		
	def add(self,*args):
		if len(args)==3:
			pos,sec,loc=args
			con=sec(loc)
		elif len(args)==2:
			pos,sec=args
			con=sec(self.value)
		else:
			raise ValueError('Not enought data.')
		self.value=self.value[:pos+1]+con+self.value[pos:]
	def del(self,pos):
		self.value=self.value[:pos()[0]+1]+self.value[pos()[1]:]
	def tran(self,tr):
		self.value=tr(self.value)
	def sub(self,*args):
		if len(args)==3:
			pos,sec,loc=args
			con=sec(loc)
		elif len(args)==2:
			pos,sec=args
			con=sec(self.value)
		else:
			raise ValueError('Not enought data.')
		self.value=self.value[:pos()[0]+1]+con+self.value[pos()[1]:]
	def tag(self,name,pos):
		self.add(pos[0],lambda x: '$tag:'+name+'&')
		self.add(pos[1],lambda x: '&tag:'+name+'$')
	def stag(self,name,pos):
		self.add(pos,lambda x: '$stag:'+name+'$')
		


def get_frist_tag(l,name):
	res=l.value.find('$tag:'+name+'&')
	if res!=-1:
		pos=res
		res=l.value.find('&tag:'+name+'$')
		if res!=-1:
			pos=(pos,res)

		return -1,'\n tag open: returning -1'
	return -1,'\n tag search inconcludent: returning -1'

def get_tags(l,namepldr):
	prov=[]
	name=namepldr
	while True:
		inn,out=get_frist_tag(l,name)
		if inn!=-1:
			prov.extend([inn,out])
			name=name[out:]
		else:
			break
	return prov
	
get_stags=lambda l,name: [m.start() for m in re.finditer('$stag:'+name+'$',l.value)]


	
			
			
			
			
			
			
			
			
			
			
