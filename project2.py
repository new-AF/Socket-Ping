import Tkinter as t
import time
top = t.Tk()
def res(e):
    #print (dir(e),e.width,e.height)
    c['width']=e.width
    c['height']=e.height
    return False
def visible(top):
    g = top.geometry()
    g = g.replace('x','+').replace('-','+').split('+')
    g = map(int,g)[0:2]
    print (g)
    w,h = g
    top.my_width = w
    top.my_half = int(w/2)
    top.my_height = h

    top.unbind('<Visibility>')
    #set_canvas(top)
    #br = Bar(c)
    b = Bar2(top,highlightcolor='red',relief='raised',bd=5,bg = 'green',width =5,height = 10,text='')


    b2 = Bar2(top,(10,10),highlightcolor='red',relief='raised',bd=5,bg = 'green',width =5,height = 10,text='')

    def move(e):
        if e.x - top.my_half > 0:
            g = b
        else:
            g = b2
        g.place(x = g.x, y=e.y-75)
    top.bind('<Motion>',move)

    def click(e):
        ball = Ball(top,(e.x,e.y),target = (b,b2)  )
    top.bind('<ButtonRelease>',click)
##    top2 = t.Toplevel()
##    top2.title(top.title())
c = t.Canvas(top)
c.pack(side=t.TOP,fill=t.BOTH,expand=1)

##class Active:
##    def __init__(self,target,criteria):
##        self.one,self.two = target
##        self.widget,self.function = criteria
##    def get(self):
##        return self.one if self.function(self.widget) else self.two
class Bar:
    def __init__(self,parent,inset=(-10,-10)):
        self.parent = parent
        self.px = 10
        self.py = 10
        self.pw = 50
        self.ph = 100
        x,y = inset
        if x<0:
            x = top.my_width + x - self.pw
            self['text'] = 'right'
        else:
            self['text'] = 'left'
        if y<0:
            y= top.my_height + y- self.ph
        self.x = x
        self.y = y
        """position: (tuple) (position_string =="""
        self.r=parent.create_rectangle(x,y,x+self.pw,y+self.ph,fill='green',outline='black')
        parent.tag_bind(self.r,'<Motion>',self.move)
        self.place(x=x,y=y)
    def move(self,e):
        self.parent.coords(self.r,self.x,e.y-30,self.y,e.y+30)

class Bar2(t.Button):
    def __init__(self,parent,inset=(-10,-10),**kw):
        self.parent = parent
        self.px = 10
        self.py = 10
        self.pw = 50
        self.ph = 100
        x,y = inset

        t.Button.__init__(self,parent,anchor='nw',**kw)
        if x<0:
            x = top.my_width + x - self.pw
            self['text'] = 'right'
        else:
            self['text'] = 'left'
        if y<0:
            y= top.my_height + y- self.ph
        self.x = x
        self.y = y

        self.place(x = x,y = y)
        self.bind('<Visibility>',self.visible)
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
        self['bitmap'] = 'error'
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
        if self.x >= self.parent.my_width or self.x <= 0:
            self.incx *= -1

        if  self.collide(0) or self.collide(1):
            self.incx *= -1
            #print (time.clock(),'collision')

        if self.y >= self.parent.my_height or self.y <= 0:
            self.incy *= -1

        self.place(x=self.x,y=self.y)
        if self.moving:
            self.after(20,self.start)

    def pause(self):
        self.moving = False
top.title("Socket Ping")
##U+2589

detour = lambda i: visible(top)
top.bind('<Visibility>',detour)
##top.bind('<Configure>',res)
top['cursor']='plus'
top.tk_bisque()
top.mainloop()