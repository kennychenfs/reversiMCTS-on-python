from __future__ import division
from random import randrange
from copy import deepcopy
from math import sqrt
class textcolor:
	bg   ="\x1b[48;5;"
	color="\x1b[38;5;"
	end  ="m"
	reset="\x1b[0m"
class nodes:
	under = []
	on = None
	win = 0
	search = 0
	color=0
	x=0
	y=0
	def __init__(self,a,b):
		self.x=a
		self.y=b
		self.under=[]
		self.win = 0
		self.search = 0
	def sort(self):
		under2=[]
		for i in range(len(self.under)):
			under2.append([self.under[i].win/self.under[i].search+0.5*(sqrt(self.search)/(self.under[i].search+1)),self.under[i]])
		under2.sort(key=lambda a:a[0],reverse=True)
		for i in range(len(self.under)):
			self.under[i]=under2[i][1]
	def printtree(self,pre):
		print('pre=%s,x=%d,y=%d,color=%d,win/search=%d/%d=%f'%(pre,self.x,self.y,self.color,self.win,self.search,self.win/self.search))
		for i in range(len(self.under)):
			self.under[i].printtree(pre+str(i)+',')
			print 'i='+str(i)
	def backup(self):
		if(self.on==None):
			return
		self.on.win=self.on.search=0
		for i in self.on.under:
			self.on.win+=self.win
			self.on.search+=self.search
		if(self.on!=None):
			self.on.backup()
	def gotoleaf(self,board):
		while not(len(self.under)==0):
			self=self.under[0]
			board.allplay(self.x,self.y,board.color)
		return self
class board:
	grid=[]
	color=0
	def __init__(self):
		for x in range(8):
			self.grid.append([])
			for y in range(8):
				self.grid[x].append(0)
		self.grid[3][3]=self.grid[4][4]=2
		self.grid[3][4]=self.grid[4][3]=1
		self.color=1
	def copy(self,origin):
		for x in range(8):
			for y in range(8):
				self.grid[x][y]=origin.grid[x][y]
		self.color=origin.color
	def allplay(self,x,y,color):
		global step
		self.grid[x][y]=color
		tx=ty=0
		for i in range(8):
			tx=x+step[i][0]
			ty=y+step[i][1]
			if tx>7 or ty>7 or tx<0 or ty<0 or self.grid[tx][ty]!=(not(color-1))+1:
				continue
			while tx>-1 and ty>-1 and tx<8 and ty<8 and self.grid[tx][ty]==(not(color-1))+1:
				tx+=step[i][0]
				ty+=step[i][1]
			if tx>7 or ty>7 or tx<0 or ty<0 or self.grid[tx][ty]!=color:
				continue
			tx-=step[i][0]
			ty-=step[i][1]
			while tx>-1 and ty>-1 and tx<8 and ty<8 and self.grid[tx][ty]==(not(color-1))+1:
				self.grid[tx][ty]=color
				tx-=step[i][0]
				ty-=step[i][1]
			continue
		self.color=(not(self.color-1))+1
	def dump(self):
		a='  0 1 2 3 4 5 6 7\n'
		for x in range(8):
			a+=str(x)
			for y in range(8):
				if self.grid[x][y]==0:
					a=a+textcolor.color+'172'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
				elif self.grid[x][y]==1:
					a=a+textcolor.color+'16'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
				else:
					a=a+textcolor.color+'255'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
			a=a+'\n'
		print (u'{}'.format(a))
	def whowin(self):
		b=w=0
		for x in range(8):
			for y in range(8):
				if self.grid[x][y]==1:
					b+=1
				if self.grid[x][y]==2:
					w+=1
		if b+w==64:
			if b>w:
				return 1
			elif b<w:
				return 2
			else:
				return 0
		else:
			return 3
	def ok(self,x,y,color):
		if not self.grid[x][y]==0:
			return 0
		tx=ty=0
		for i in range(8):
			tx=x+step[i][0]
			ty=y+step[i][1]
			if tx>7 or ty>7 or tx<0 or ty<0 or self.grid[tx][ty]!=(not(color-1))+1:
				continue
			while(tx>-1 and ty>-1 and tx<8 and ty<8 and (self.grid[tx][ty]==(not(color-1))+1)):
				tx+=step[i][0]
				ty+=step[i][1]
			if tx>-1 and ty>-1 and tx<8 and ty<8 and self.grid[tx][ty]==color:
				return 1
		return 0
	def possible(self):
		psb=[]
		for x in range(8):
			for y in range(8):
				if self.ok(x,y,self.color):
					psb.append([x,y])
		return psb
	def reversecolor(self):
		self.color=(not(self.color-1))+1
step=[[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
gameboard=board()
root=nodes(-1,-1)
def visit(node):
	nonetimes=0
	startboard=board()
	startboard.grid=deepcopy(gameboard.grid)
	startboard.color=deepcopy(gameboard.color)
	node=node.gotoleaf(startboard)
	psb=startboard.possible()
	for i in psb:
		node.under.append(nodes(i[0],i[1]))
	for searchnode in node.under:
		searchnode.on=node
		searchnode.color=startboard.color
		for i in range(10):
			searchboard=board()
			searchboard.grid=deepcopy(startboard.grid)
			searchboard.color=deepcopy(startboard.color)
			searchboard.allplay(searchnode.x,searchnode.y,searchboard.color)
			win=searchboard.whowin()
			nonetimes=0
			while win==3:
				psb=searchboard.possible()
				if len(psb)==0:
					if nonetimes==0:
						nonetimes=1
						searchboard.color=(not(searchboard.color-1))+1
						continue
					else:
						win=0
						break
				tmp=randrange(0,len(psb))
				searchboard.allplay(psb[tmp][0],psb[tmp][1],searchboard.color)
				win=searchboard.whowin()
			if win == gameboard.color:
				searchnode.win+=1
			searchnode.search+=1
		searchnode.backup()
	node.sort()
	while node.on!=None:
		node=node.on
		node.sort()
def player():
	global root
	gameboard.dump()
	x=int(input('x?'))
	y=int(input('y?'))
	gameboard.allplay(x,y,2)
	gameboard.dump()
	root.printtree('')
	for i in root.under:
		if i.x==x and i.y==y:
			root=i
			break
	if(gameboard.whowin()==3):
		mcts()
def mcts():
	global root
	for i in range(50):
		print ('%3.1f%%'%(i/50*100))
		visit(root)
	root=root.under[0]
	gameboard.dump()
	gameboard.allplay(root.x,root.y,1)
	if(gameboard.whowin()==3):
		player()
mcts()
