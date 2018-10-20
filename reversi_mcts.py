class textcolor:
	bg   ="\x1b[48;5;"
	color="\x1b[38;5;"
	end  ="m"
	reset="\x1b[0m"
class nodes:
	under = []
	on = None
	x = None
	y = None
	win = 0
def dump():
	a=''
	for x in range(8):
		for y in range(8):
			if board[x][y]==0:
				a=a+textcolor.color+'172'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
			elif board[x][y]==1:
				a=a+textcolor.color+'16'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
			else:
				a=a+textcolor.color+'255'+textcolor.end+textcolor.bg+'172'+textcolor.end+u'\u25cf '+textcolor.reset
		a=a+'\n'
	print (u'{}'.format(a))
step=[[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]];
board=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,2,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
root=nodes()
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
		while board[tx][ty]==(not(color-1))+1 and tx>-1 and ty>-1 and tx<8 and ty<8:
			tx+=step[i][0]
			ty+=step[i][1]
		if tx>-1 and ty>-1 and tx<8 and ty<8 and board[tx][ty]==color:
			return 1
	return 0
def possible(color):
	psb=[[]]
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
		while board[tx][ty]==(not(color-1))+1 and tx>-1 and ty>-1 and tx<8 and ty<8:
			tx+=step[i][0]
			ty+=step[i][1]
		if tx>7 or ty>7 or tx<0 or ty<0 or board[tx][ty]!=color:
			continue
		tx-=step[i][0]
		ty-=step[i][1]
		while board[tx][ty]==(not(color-1))+1 and tx>-1 and ty>-1 and tx<8 and ty<8:
			board[tx][ty]=color
			tx-=step[i][0]
			ty-=step[i][1]
		continue
def mcts(color):
	global root
	psb=possible(color)
	
