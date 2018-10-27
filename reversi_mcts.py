from __future__ import division
from random import randint
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
			under2.append([self.under[i].win/self.under[i].search,self.under[i]])
		under2.sort(key=lambda a:a[0],reverse=True)
		for i in range(len(self.under)):
			self.under[i]=under2[i][1]
	def printtree(self,pre):
		print('pre=%s,x=%d,y=%d,color=%d,win/search=%d/%d'%(pre,self.x,self.y,self.color,self.win,self.search))
		for i in range(len(self.under)):
			self.under[i].printtree(pre+str(i)+',')
			print 'i='+str(i)
def dump(areaboard):
	a=''
	for x in range(8):
		for y in range(8):
			if areaboard[x][y]==0:
				a=a+textcolor.color+'172'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
			elif areaboard[x][y]==1:
				a=a+textcolor.color+'16'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
			else:
				a=a+textcolor.color+'255'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
		a=a+'\n'
	print (u'{}'.format(a))
step=[[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]];
board=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,2,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
root=nodes(-1,-1)
def initboard(board):
	for x in range(8):
		for y in range(8):
			board[x][y]=0
	board[3][3]=board[4][4]=1
	board[3][4]=board[4][3]=2
def ww():
	b=w=0
	for x in range(8):
		for y in range(8):
			if board[x][y]==1:
				b+=1
			if board[x][y]==2:
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
def ok(x,y,color):
	if not board[x][y]==0:
		return 0
	tx=ty=0
	for i in range(8):
		tx=x+step[i][0]
		ty=y+step[i][1]
		if tx>7 or ty>7 or tx<0 or ty<0 or board[tx][ty]!=(not(color-1))+1:
			continue
		while(tx>-1 and ty>-1 and tx<8 and ty<8 and (board[tx][ty]==(not(color-1))+1)):
			tx+=step[i][0]
			ty+=step[i][1]
		if tx>-1 and ty>-1 and tx<8 and ty<8 and board[tx][ty]==color:
			return 1
	return 0
def possible(color):
	psb=[]
	for x in range(8):
		for y in range(8):
			if ok(x,y,color):
				psb.append([x,y])
	return psb
def allplay(x,y,color):
	board[x][y]=color
	tx=ty=0
	for i in range(8):
		tx=x+step[i][0]
		ty=y+step[i][1]
		if tx>7 or ty>7 or tx<0 or ty<0 or board[tx][ty]!=(not(color-1))+1:
			continue
		while tx>-1 and ty>-1 and tx<8 and ty<8 and board[tx][ty]==(not(color-1))+1:
			tx+=step[i][0]
			ty+=step[i][1]
		if tx>7 or ty>7 or tx<0 or ty<0 or board[tx][ty]!=color:
			continue
		tx-=step[i][0]
		ty-=step[i][1]
		while tx>-1 and ty>-1 and tx<8 and ty<8 and board[tx][ty]==(not(color-1))+1:
			board[tx][ty]=color
			tx-=step[i][0]
			ty-=step[i][1]
		continue
def visit(node,color):
	global board
	dump(board)
	print'this is visit'
	startcolor=color
	win=3
	nonetimes=0
	while not node.under==[]:
		node=node.under[0]
		allplay(node.x,node.y,node.color)
		startcolor=(not(startcolor-1))+1
		dump(board)
	originboard=[]
	for x in range(8):
		originboard.append([])
		for y in range(8):
			originboard[x].append(board[x][y])
	startpsb=possible(color)
	for i in startpsb:
		tmp=nodes(i[0],i[1])
		node.under.append(tmp)
	for searchnode in node.under:
		searchnode.on=node
		searchcolor=startcolor
		allplay(searchnode.x,searchnode.y,startcolor)
		for i in range(50):
			searchcolor=(not(startcolor-1))+1
			searchpossible=possible(searchcolor)
			win=3
			while ww()==3:
				if(len(searchpossible)==0):
					if(nonetimes>0):
						win=0
						break
					else:
						nonetimes+=1
						continue
				tmp=randint(0,len(searchpossible)-1)
				allplay(searchpossible[tmp][0],searchpossible[tmp][1],searchcolor)
				searchcolor=(not(searchcolor-1))+1
				searchpossible=possible(searchcolor)
			if not (ww()==3):
				win=ww()
			if win == color:
				searchnode.win+=1
			searchnode.search+=1
			board=[]
			for x in range(8):
				board.append([])
				for y in range(8):
					board[x].append(originboard[x][y])
			allplay(searchnode.x,searchnode.y,startcolor)
		searchnode.color=searchcolor
	for i in node.under:
		node.win+=i.win
		node.search+=i.search
	node.sort()
#	print('root.win=%d,root.search=%d'%(root.win,root.search))
	return
def mcts():
	for i in range(10):
		initboard(board)
		visit(root,1)
mcts()
root.printtree('')
