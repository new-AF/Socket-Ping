import Tkinter as t
import time
#import asyncio
#import websockets
from PIL import ImageTk,Image
import socketio


sio = socketio.Client()




top = t.Tk()
Pos = ''


@sio.event
def connect(data = None):
    sio.emit('get_my_name')


@sio.event
def my_name(data):
    global Pos
    Pos = data
    print ('my_name',data)

sio.connect('http://damp-basin-29915.herokuapp.com')
#sio.connect('http://localhost:5000')

def tk_image(fname,*rest ):
    p = Image.open(fname) # pillow_image

    if rest:
        p = p.resize(rest[0:2])

    i = ImageTk.PhotoImage(p)
    return i


def put():
    b = Bar2(top,highlightcolor='red',relief='raised',bd=5,bg = 'green',width =5,height = 10,text='')

    b2 = Bar2(top,(10,10),highlightcolor='red',relief='raised',bd=5,bg = 'green',width =5,height = 10,text='')

    top.my_half = top.winfo_width() / 2

    top.Vline = t.Label(top,text='',bg='gray80',width=1)
    def move(e):
        if e.x - top.my_half > 0:
            g = b
        else:
            g = b2
        g.place(x = g.x, y=e.y-75)
    top.bind('<Motion>',move)

    @sio.event
    def move2(e,serv = 0):
        g = [b,b2] [Pos]
        inc = 10
        if e.keysym.lower() == 'up':
            inc = -10

        elif e.keysym.lower() == 'down':
            inc = 10

        sio.emit('save',{'Pos':Pos,'inc':inc})

    @sio.event
    def move3(data):

        pos = data['Pos']
        inc = data['inc']

        g = [b,b2] [pos]

        g.y += inc
        b.place(x=g.x , y = g.y)


    top.bind('<KeyPress>',move2)
    def click(e):
        ball = Ball(top,(e.x,e.y),target = (b,b2)  )
    top.bind('<ButtonRelease>',click)

    top.Vline.place(relx=0.5,rely=0,relheight=1,anchor=t.N)
class Bar:
    def __init__(self,parent,inset=(-10,-10),**kw):
        self.parent = parent
        self.px = 10
        self.py = 10
        self.pw = 50
        self.ph = 100
        x,y = inset
        if x<0:
            x = top.winfo_width()  + x - self.pw
            self['text'] = 'right'
        else:
            self['text'] = 'left'
        if y<0:
            y= top.winfo_height() + y- self.ph

        self.x = x
        self.y = y
        """position: (tuple) (position_string =="""
        self.r=parent.create_rectangle(x,y,x+self.pw,y+self.ph,fill='green',outline='black')
        parent.tag_bind(self.r,'<Motion>',self.move)
        self.place(x=x,y=y)
    def move(self,e):
        self.parent.coords(self.r,self.x,e.y-30,self.y,e.y+30)

class Bar2(t.Label):
    def __init__(self,parent,inset=(-10,-10),**kw):
        self.parent = parent
        self.px = 10
        self.py = 10
        self.pw = 50
        self.ph = 100
        x,y = inset

        t.Label.__init__(self,parent,anchor='nw',**kw)
        if x<0:
            x = top.winfo_width() + x - self.pw

            self.num = 0
        else:

            self.num = 1

        self['text'] = ['right','left'][self.num]

        self.x = x
        self.y = y

        self.place(x = x,y = y)
        self.bind('<Visibility>',self.visible)

        self.put_scores_on_screen()

    def get_score(self,x):
        return getattr(top,'Xscr%d'%x)

    def put_scores_on_screen(self):


        self.all_num = [top.Xvar0,top.Xvar1]
        self.all_scr = [top.Xscr0,top.Xscr1]

        self.name_var = self.all_num[self.num]
        oppo = int (not self.num)

        self.player_label = t.Label(top,text = self.name_var.get(),font = 'system 20 bold')
        pos = [(t.N+t.W,0.05),(t.N+t.E,0.95)][self.num-1]

        self.player_label.place(relx = pos[1],rely=0.0,anchor = pos[0])

        self.score_label = t.Label(top,textvariable = self.get_score(oppo),font = 'system 20 bold')

        self.score_label.place(relx = pos[1],y=self.score_label.winfo_reqheight()+5,anchor = pos[0])
    def visible(self,e):

        self.width,self.height = (self.winfo_width(),self.winfo_height())
        self.unbind('<Visibility>')
##        parent.bind('<Motion>',self.move)

##    def move(self,e):
##        #print (e.x,e.y)
##        print (self['text'])
##        #print (e.widget)
##        #print e.x - self.parent.my_half
####            self.place(x = self.x, y = e.y - 85)

class Ball(t.Button):

    def __init__(self,parent,coordinates = (0,0),**kw):

        self.target = kw.pop('target')
        self.parent = parent
        t.Button.__init__(self,parent,anchor='nw',**kw)
        self.image = tk_image('4.png')
        self['image'] = self.image
        self['relief'] = 'flat'

        self.x , self.y = coordinates
        self.incx = 3
        self.incy = 3
        self.place(x=self.x,y=self.y)
        self.moving = 1
        self.start()

    def collide(self,side = 0):
        target = self.target[side]

        x,y = self.x, self.y
        w = self.winfo_width()
        h = self.winfo_height()

        tx,ty = target.winfo_x(), target.winfo_y()
        th, tw = target.height, target.width

##        if side == 0:
##            c1 = x + w > tx
##        elif side ==1:
##            c1 = x + w < tx+tw
        c1 = abs((x+w/2) - (tx + tw/2)) <= 5
        c2 = y + h >= ty and y+h <= ty + th

        return c1 and c2
    def start(self):
        self.x += self.incx
        self.y +=self.incy
##        print (self.target[0]['text'])
        #print (self.target[0].winfo_x(),self.target[0].winfo_y(),'collision')
        #target = self.target.get()
        if self.x >= self.parent.winfo_width():
            top.Xscr0.set(top.Xscr0.get()+1)
            self.incx *= -1
        if self.x <= 0:
            top.Xscr1.set(top.Xscr1.get()+1)
            self.incx *= -1
            #self.target
        if  self.collide(0) or self.collide(1):
            self.incx *= -1
            #print (time.clock(),'collision')
            #top.bell()

        if self.y >= self.parent.winfo_height() or self.y <= 0:
            self.incy *= -1

        self.place(x=self.x,y=self.y)
        if self.moving:
            self.after(20,self.start)

    def pause(self):
        self.moving = False

class Intro(t.Frame):
    def __init__(self,parent = None):
        t.Frame.__init__(self,parent if parent else top)
        self.pack(side=t.TOP,fill='both',expand = 1)
        s = self

        s.bind("<Visibility>", s.put_on_screen)

        top.Xvar0=t.StringVar()
        top.Xvar1 = t.StringVar(value='Player2')
        top.Xscr0 = t.IntVar(value=0)
        top.Xscr1 = t.IntVar(value=0)
        self.ee = t.Label(self,text='',font = 'system 20')
        c = self.c = t.Label(self,text = 'Enter your Name', font = 'system 20 bold', anchor = t.N)
        self.title = t.Label(self,padx=10,pady=10,relief='groove',bd=10,text = 'Sockets Ping Pong', font = 'system 30 bold', anchor = t.N)
        self.text= t.Entry(self,textvariable=top.Xvar1,bg = top['bg'],insertborderwidth = 5, justify=t.CENTER, font = 'system 20 bold')
        self.text.bind('<KeyPress-Return>',self.entered)
        #print (c.winfo_width(),c.winf)

    def entered(self,e):
        name = top.Xvar1.get()
        #print (name)
        #print ('***',top.pack_slaves())
        self.pack_forget()
        #print ('***',top.pack_slaves())
        sio.emit('')
        put()

    def put_on_screen(self,e):
        c = self.c

        w,h = c.winfo_width(),c.winfo_height()

        self.title.pack(pady= '0.5i',side =  t.TOP,fill = t.X,expand = 1)
        self.ee.pack(pady='0.1i',fill = t.X,expand = 1)
        self.text.pack(pady='0.5i',side =  t.BOTTOM,fill = t.X,expand = 1)
        self.c.pack(side =  t.BOTTOM,fill = t.X,expand = 1)
        self.text.focus()

class PList(t.Frame):
    def __init__(self,p=top,**kw):
        self.parent = p
        t.Frame.__init__(self,self.parent)
        self.a = []
        self.pack(fill='both',expand = 1)
        self.add('Pick an opponent',None)
        self.add('',None)
        self.add('23')


    def add(self,text,cur = 'hand2'):
        item = t.Label(self,text=text,font = 'system 20 bold')
        if cur:
            item['cursor'] = cur
            item.bind('<ButtonRelease>',self.click)
        self.a += [item]
        item.pack(fill='x',expand=1)


    def click(self):
        pass
intro = Intro()
top.title("Sockets Ping Pong")
##U+2589
##detour = lambda i: put()
##top.bind('<Visibility>',detour)
##top.bind('<Configure>',res)
top['cursor']='plus'
top.tk_bisque()
top.mainloop()