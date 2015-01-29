#!/usr/bin/python

#chat module

import cPickle as pickle

def hash2col(h):
	fcol = int(h[:6],16)
	fcol = (fcol)/2 + 0x888888
	return "#%06x"%fcol

class Chat:
	def __init__(self,fname):
		self.fname = fname
		
		try:
			f = open(self.fname,'rw')
			self.opened = False
			f.close()
		except IOError:
			self.opened = True
			self.data = []
		
			
	def pushm(self, sender, color, message, date):
		
		
		f = open(self.fname,'r')
		self.data = pickle.load(f)
		f.close()
		
		self.data.append( (sender,color,message,date))
		
		f = open(self.fname,'w')
		pickle.dump(self.data, f)
		f.close()
	
	def getFormat(self):
		
		try:
			f = open(self.fname,'r')
			self.data = pickle.load(f)
			f.close()
		except IOError:
			self.data = []
		
		out = ""
		
				
		for l in self.data:
			
			if (l[0] == "Guest"):
				tag = l[0]
			else:
				tag = '''<b style="color:%s; text-shadow: 1px 1px #eeeeee">%s</b>'''%(l[1],l[0])

			out+='''<div class="row">
			<p><big>%s: %s</big></p>
			
			</div>'''%(tag,l[2])
		
		return out
		
