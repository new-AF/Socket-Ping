import Tkinter as t
import time , socketio

from PIL import ImageTk,Image
 

class App(t.Tk):
	def __init__(self,ip):
		t.Tk.__init__(self)
		self.title('Sockets ping pong')
		#self.pos = [None,'Left','Right'][p]
		
		self.tk_bisque()
		self.ip = ip

		self.intro()
		self.geometry('400x400+500+500')
		self.mainloop()
	
	def connect(self,e):
		print("connecting ...")
		self.socket = socketio.Client()
		self.socket.on('connect',self.connected)
		self.socket.connect(self.ip)
		
	
	def connected(self):
		print ('connected',self)
		self.playshow()
	
	def playshow(self):
		pass
	
	def intro(self):
		try:
			self.f1
		except:
			self.f1 = t.Frame(self)
			self.l1 = t.Label(self.f1,text='sockets ping pong',font = 'system 20 bold')
			self.l2 = t.Label(self.f1,text='connecting to server at\n{}'.format(self.ip),font = 'system 20 bold')
			self.l3 = t.Label(self.f1,text='Enter your name',font = 'system 20 bold')
			self.t1 = t.Entry(self.f1)
			self.t1.bind('<KeyRelease>',self.connect)
			for i in ('f1 l1 l2 l3 t1'.split() ):
				w = getattr(self,i)
				w.pack(fill='x',expand=1)
				
			
			
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
