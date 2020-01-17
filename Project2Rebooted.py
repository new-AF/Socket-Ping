import Tkinter as t
import time , socketio

from PIL import ImageTk,Image
 

class App:
	def __init__(self,ip):
		self.top = t.Tk()
		self.top.title('Sockets ping pong')
		#self.pos = [None,'Left','Right'][p]
		
		self.top.tk_bisque()
		self.ip = ip
		
		self.intro()
		self.top.protocol("WM_DELETE_WINDOW",self.disconnect)
		self.top.geometry('400x400+500+500')
		self.top.mainloop()
	
	def disconnect(self):
		try:
			self.socket.disconnect()
		except:
			pass
		self.top.destroy()
	
	def connect(self,e):
		self.l2['text'] = 'Connecting ... to'
	
		self.socket = socketio.Client()
		self.socket.on('connect',self.connected)
		self.socket.on('my_name',self.my_name)
		self.socket.on('getmoved',self.getmoved)
		self.socket.on('startBall',self.startBall)
		self.socket.on('getupdated',self.getupdated)
		self.socket.connect(self.ip)
		#self.connected()
		
	def my_name(self,data):
		d = data
		#print 'got',data,type(data)
		self.l2['text']= 'Connection Established !'
		#self.l3['label'] = 'Press Enter to Proceed'
		self.top.after(500,self.playshow,0,d)
		#self.playshow(side = d)
	
	def connected(self):
		#print ('connected',self)
		self.socket.emit('get_my_name')
		
		
	def getmoved(self,data):
		own,other = data
		w = [self.p1,self.p2][own]
		#print ('own',own,'other',other)
		w.place(y = other)
		
	def moveup(self,e):
		w = self.own
		try:
			self.y
		except:
			self.y = w.winfo_y()
		self.y += -5
		self.socket.emit('move',[self.owncode,self.y])
		
	
	def movedo(self,e):
		w = self.own
		try:
			self.y
		except:
			self.y = w.winfo_y()
		self.y += 5
		self.socket.emit('move',[self.owncode,self.y])
		#w.place(y = self.y)
	
	def playshow(self, hide=0 , side = 0):
		try:
			self.p1	#paddle 1 / bar1
		except:
			self.intro(hide = 1)
			self.p1 = t.Button(self.top,text='Left',height = 15,bg='green', width= 8)
			self.p2 = t.Button(self.top,text='Right',height = 15,bg='green', width = 8)
			self.p1.svar = t.StringVar()
			self.p2.svar = t.StringVar()
			self.p1.ivar = t.IntVar(0)
			self.p2.ivar = t.IntVar(0)
			self.score1 = t.Label(self.top,textvariable = self.p1.ivar,font = 'system 20')
			self.score2 = t.Label(self.top,textvariable = self.p2.ivar,font = 'system 20')
			self.s1 = t.Label(self.top,textvariable = self.p1.svar,font = 'system 20')
			self.s2 = t.Label(self.top,textvariable = self.p2.svar,font = 'system 20')
			self.own = [self.p1,self.p2] [side]
			self.owncode = side
			self.top.title('{}'.format(self.own['text']))
			self.other = [self.p1,self.p2] [not side]
			
			#self.socket.emit('update_score',self.owncode)
		
			self.top.bind('<KeyPress-Up>',self.moveup)
			self.top.bind('<KeyPress-Down>',self.movedo)
			#self.scores()
			#self.top.bind('KeyRelease-Return',startball)
			
		if hide:
			for i in (self.p1,self.p2):
				i.place(relheight=0,relwidth=0)
		else:
			self.p1.place(relx = 0.1, rely=0.2,anchor = 'nw')
			self.p2.place(relx = 0.9, rely=0.2,anchor = 'ne')
			self.s1.place(relx = 0.2,rely = 0.01, anchor = 'n')
			self.s2.place(relx = 0.8,rely = 0.01, anchor = 'n')
			self.score1.place(relx = 0.2,rely = 0.1, anchor = 'n')
			self.score2.place(relx = 0.8,rely = 0.1, anchor = 'n')
			#self.socket.emit('startBall')
			self.y = self.own.winfo_y()
			self.startBall()
	
	def intro(self,hide = 0):
		try:
			self.f1
		except:
			self.f1 = t.Frame(self.top)
			self.l1 = t.Label(self.f1,padx=10,pady=10,relief='groove',bd=10,text='Sockets ping pong',font = 'system 30 bold')
			self.l2 = t.Label(self.f1,text='Press Enter to connect to server @',font = 'system 10 bold')
			self.l3 = t.Label(self.f1,text='{}'.format(self.ip),font = 'system 10 bold')
			self.name = t.StringVar()
			self.t1 = t.Label(self.f1,text = 'github.com/new-AF',font = 'system 10 bold',relief = 'groove')
			self.top.bind('<KeyRelease-Return>',self.connect)
			
			for i in ('l1 l2 l3 t1'.split() ):
				w = getattr(self,i)
				w.pack(fill='x',expand=1)
		
		if hide:
			#self.f1.place(x=0,y=0,relheight=0,relwidth=0)
			self.f1.destroy()
		else:
			self.f1.place(x=0,y=0,relwidth=1,relheight=1)
			self.t1.focus()
	
	def createBall(self, w = 20, h= 20):
		try:
			self.ballW
		except:
			self.ballW = t.Canvas(self.top, width = w, height = h, relief= 'flat',borderwidth = 0)
			self.ballW.create_oval( 0,0,w,h, fill = 'black')

	def startBall(self, hide=0,reset = 0):
		self.ball = [  self.top.winfo_width()/2 , self.top.winfo_height()/2 ]
		self.ball = map(int,self.ball)
		self.Inc = [3, 3]
		
		if reset:
			return
		try:
			self.ballW
		except:
			self.createBall()
	
		self.moveBall()
	
	def moveBall(self):
		try:
			self.moving
		except:
			self.moving = 1
		
		if self.moving:
			x,y = self.ball
			self.ballW.place( x = self.ball[0] , y = self.ball[1] )
			
			if self.collide(self.own) or self.collide(self.other):
				self.Inc[0] *= -1
			
			if x >= self.top.winfo_width() or x<=0:
				self.sendScore(x)
				self.startBall(0,1)
			
			if y >= self.top.winfo_height() or y<=0:
				self.Inc[1] *= -1
			
			self.ball[0] += self.Inc[0]
			self.ball[1] += self.Inc[1]
			self.top.after(30, self.moveBall )
		
	def collide(self,tar):

		x,y = self.ball
		w = self.ballW.winfo_width()
		h = self.ballW.winfo_height()

		tx,ty = tar.winfo_x(), tar.winfo_y()
		th, tw = tar.winfo_height(), tar.winfo_width()

		c1 = abs((x+w/2) - (tx + tw/2)) <= 5
		c2 = y + h >= ty and y+h <= ty + th

		return c1 and c2
	
	def getupdated(self,data):
		d = data
		w = [self.own,self.other][not d]
		old = w.ivar.get()
		w.ivar.set(old+1)
	
	def sendScore(self,x):
		#print 'sending score'
		self.socket.emit('update_score', (x < self.top.winfo_width()/2) and self.owncode  )

if __name__ == '__main__':
    App(ip = 'http://damp-basin-29915.herokuapp.com')
