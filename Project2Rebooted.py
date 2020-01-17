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
		print("connecting ...")
	
		self.socket = socketio.Client()
		self.socket.on('connect',self.connected)
		self.socket.on('my_name',self.my_name)
		self.socket.on('getmoved',self.getmoved)
		self.socket.connect(self.ip)
		#self.connected()
		
	def my_name(self,data):
		d = data
		print 'got',data,type(data)
		self.top.after(500,self.playshow,0,d)
		#self.playshow(side = d)
	
	def connected(self):
		print ('connected',self)
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
			self.p1 = t.Button(self.top,text='Left',height = 25,bg='blue', width= 10)
			self.p2 = t.Button(self.top,text='Right',height = 25,bg='blue', width = 10)
			
			self.own = [self.p1,self.p2] [side]
			self.owncode = side
			self.top.title('{}'.format(self.owncode))
			self.other = [self.p1,self.p2] [not side]
				
		
		
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
			
			
	def intro(self,hide = 0):
		try:
			self.f1
		except:
			self.f1 = t.Frame(self.top)
			self.l1 = t.Label(self.f1,text='sockets ping pong',font = 'system 20 bold')
			self.l2 = t.Label(self.f1,text='connecting to server at\n{}'.format(self.ip),font = 'system 20 bold')
			self.l3 = t.Label(self.f1,text='Enter your name',font = 'system 20 bold')
			self.name = t.StringVar()
			self.t1 = t.Entry(self.f1,textvariable = self.name)
			self.t1.bind('<KeyRelease-Return>',self.connect)
			
			for i in ('l1 l2 l3 t1'.split() ):
				w = getattr(self,i)
				w.pack(fill='x',expand=1)
		
		if hide:
			#self.f1.place(x=0,y=0,relheight=0,relwidth=0)
			self.f1.destroy()
		else:
			self.f1.place(x=0,y=0,relwidth=1,relheight=1)
			self.t1.focus()
	
	def startball(self,begin = 0):
		try:
			self.ballxy
		except:
			self.ballxy = [int(self.top.winfo_width()/2),int(self.top.winfo_height()/2)]
		
		if begin:
			pass
			
'''
A = None

@socket.event
def connect(data = None):
    socket.emit('get_my_name')


@socket.event
def my_name(data):
    global A
    print ('my_name',data)
    A = App(top,data)
    

def tk_image(fname,*rest ): #rest : resize -> tuple(w,h)
    p = Image.open(fname)

    if rest:
        p = p.resize(rest[0:2])

    i = ImageTk.PhotoImage(p)
    return i

socket.connect('http://damp-basin-29915.herokuapp.com')

top.tk_bisque()
top.mainloop()
'''
if __name__ == '__main__':
    App(ip = 'http://damp-basin-29915.herokuapp.com')
