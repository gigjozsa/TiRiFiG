# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 13:21:38 2016

@author: samuel
"""

#from tkinter import *

#root = Tk()
#w = Label(root, text="Hello Tkinter!")
#w.pack()
#root.mainloop()

#root=Tk()
#img = PhotoImage(file="/home/samuel/Documents/pythonCodes/python.gif")
#w1 = Label(root, image = img).pack(side="right")
#
#explanation="At present, only GIF and PPM/PGM formats are supported, but an interface allows for other image formats to be added easily"
#w2 = Label(root, justify = CENTER, padx=50, text = explanation).pack(side="left")
#
#root.mainloop()

#root = Tk()
#img = PhotoImage(file="/home/samuel/Documents/pythonCodes/python.gif")
#txt = "In order to display the text and the image, you need to specify center for compound"
#w = Label(root, compound = LEFT, text = txt, image = img).pack(side = "right")
#root.mainloop()

#root = Tk()
#img = PhotoImage(file="/home/samuel/Documents/pythonCodes/python.gif")
#txt = "This is another example putting the image on the right side and the text on the left"
#
#w = Label(root, justify = LEFT, compound = LEFT, padx=10, text = txt, image = img).pack(side = "right")
#
#root.mainloop()

#root = Tk()
#
#Label(root, text = "Red Text in Times Font", fg = "red", font = "Times").pack()
#Label(root, text = "Green Text in Helvetica Font", justify = RIGHT, fg = "green", bg = "light green", font = "Helvetica 16 bold italic").pack()
#Label(root, text = "Blue text in Verdana bold", justify = LEFT, fg = "blue", bg = "yellow", font = "Verdana 10 bold").pack()
#
#root.mainloop()
#import tkinter as tk
#
#counter = 0 
#def counter_label(label):
#  def count():
#    global counter
#    counter += 1
#    label.config(text=str(counter))
#    label.after(1000, count)
#  count()
# 
# 
#root = tk.Tk()
#root.title("Counting Seconds")
#label = tk.Label(root, fg="green")
#label.pack()
#counter_label(label)
#button = tk.Button(root, text='Stop', width=25, command=root.destroy)
#button.pack()
#root.mainloop()


#import tkinter as tk
#
#class TkFileDialogExample(tk.Frame):
#
#  def __init__(self, root):
#
#    tk.Frame.__init__(self, root)
#
#    # options for buttons
#    button_opt = {'fill': tk.constants.BOTH, 'padx': 5, 'pady': 5}
#
#    # define buttons
#    tk.Button(self, text='askopenfile', command=self.askopenfile).pack(**button_opt)
#    tk.Button(self, text='askopenfilename', command=self.askopenfilename).pack(**button_opt)
#    tk.Button(self, text='asksaveasfile', command=self.asksaveasfile).pack(**button_opt)
#    tk.Button(self, text='asksaveasfilename', command=self.asksaveasfilename).pack(**button_opt)
#    tk.Button(self, text='askdirectory', command=self.askdirectory).pack(**button_opt)
#
#    # define options for opening or saving a file
#    self.file_opt = options = {}
#    options['defaultextension'] = '.txt'
#    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
#    options['initialdir'] = 'C:\\'
#    options['initialfile'] = 'myfile.txt'
#    options['parent'] = root
#    options['title'] = 'This is a title'
#
#    # This is only available on the Macintosh, and only when Navigation Services are installed.
#    #options['message'] = 'message'
#
#    # if you use the multiple file version of the module functions this option is set automatically.
#    #options['multiple'] = 1
#
#    # defining options for opening a directory
#    self.dir_opt = options = {}
#    options['initialdir'] = 'C:\\'
#    options['mustexist'] = False
#    options['parent'] = root
#    options['title'] = 'This is a title'
#
#  def askopenfile(self):
#
#    """Returns an opened file in read mode."""
#
#    return tk.FileDialog.askopenfile(mode='r', **self.file_opt)
#
#  def askopenfilename(self):
#
#    """Returns an opened file in read mode.
#    This time the dialog just returns a filename and the file is opened by your own code.
#    """
#
#    # get filename
#    filename = tk.FileDialog.askopenfilename(**self.file_opt)
#
#    # open file on your own
#    if filename:
#      return open(filename, 'r')
#
#  def asksaveasfile(self):
#
#    """Returns an opened file in write mode."""
#
#    return tk.FileDialog.asksaveasfile(mode='w', **self.file_opt)
#
#  def asksaveasfilename(self):
#
#    """Returns an opened file in write mode.
#    This time the dialog just returns a filename and the file is opened by your own code.
#    """
#
#    # get filename
#    filename = tk.FileDialog.asksaveasfilename(**self.file_opt)
#
#    # open file on your own
#    if filename:
#      return open(filename, 'w')
#
#  def askdirectory(self):
#
#    """Returns a selected directoryname."""
#
#    return tk.FileDialog.askdirectory(**self.dir_opt)
#
#if __name__=='__main__':
#  root = tk.Tk()
#  TkFileDialogExample(root).pack()
#  root.mainloop()

#import Tkinter
#
#root = Tkinter.Tk()
#
#Tkinter.Label(root, text="Hello World").pack()
#
#root.mainloop()

#from tkinter import *

#class App:
#    def __init__(self,master):
#        
#        self.frame = Frame(master)
#        self.frame.pack()
#        
#        self.button = Button(self.frame, text = "Quit", fg = "red", command = self.frame.quit)
#        self.button.pack(side=LEFT)
#        
#        self.hi_there = Button(self.frame, text = "Hello", command = self.say_hi)
#        #self.hi_there.pack(side=LEFT)
#        
#    def say_hi(self):
#        print ("hi there Sam!")
#
#root = Tk()
#app = App(root)
#root.mainloop()

#root = Tk()
#
#def callback(event):
#    print ("clicked at", event.x, event.y)
#
#frame = Frame(root, width = 100, height = 100)
#frame.bind("<B1-Motion>",callback)
#frame.pack()
#
#root.mainloop()

#from tkinter import messagebox
#
#def callBack():
#    if messagebox.askokcancel("Quit","Do you really want to quit"):
#        root.destroy()
#root = Tk()
#root.protocol("WM_DELETE_WINDOW",callBack)
#
#root.mainloop()

#class MyDialog:
#    def __init__(self, parent):
#        top = self.top = Toplevel(parent)
#        Label(top, text="Value").pack()
#        self.e = Entry(top)
#        self.e.pack(padx=5)
#        b = Button(top, text="OK", command=self.ok)
#        b.pack(pady=5)
#    def ok(self):
#        print ("value is", self.e.get())
#        self.top.destroy()
#root = Tk()
#Button(root, text="Hello!").pack()
#root.update()
#d = MyDialog(root)
#root.wait_window(d.top)

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


def animate(i):
    pullData = open("/home/samuel/Documents/pythonCodes/sampleData.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)

    
            

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()