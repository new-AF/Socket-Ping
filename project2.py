import Tkinter as t

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
##    top2 = t.Toplevel()
##    top2.title(top.title())
c = t.Canvas(top)
c.pack(side=t.TOP,fill=t.BOTH,expand=1)

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
        t.Button.__init__(self,parent,**kw)
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
##        parent.bind('<Motion>',self.move)

##    def move(self,e):
##        #print (e.x,e.y)
##        print (self['text'])
##        #print (e.widget)
##        #print e.x - self.parent.my_half
####            self.place(x = self.x, y = e.y - 85)

top.title("Socket Ping")
##U+2589

detour = lambda i: visible(top)
top.bind('<Visibility>',detour)
##top.bind('<Configure>',res)
top['cursor']='plus'
top.tk_bisque()
top.mainloop()