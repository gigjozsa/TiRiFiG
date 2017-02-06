# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 01:09:38 2016

@author: samuel
"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


class fetchDefVals:
    
    def getData(path):
        with open(path) as f:
            data = f.readlines()
        return data
        
    def getParameter(sKey,data):
        for i in data:
            lineVals = i.split()
            for j in range(len(lineVals)):
                if lineVals[j]==sKey:
                    parVal = lineVals[j+1:]
                    break
                    break
        for i in range(len(parVal)):
            parVal[i]=int(parVal[i])
        return parVal        
        

def canvasVals():
    
def animate(i,y):
    for i in range(len(RADIvals)):
    RADIvals[i] = RADIvals[i] + moveVals[0]
for i in range(len(VROTval)):
    VROTval[i] = VROTval[i] + moveVals[1]
    txt = " " + str(VROTval[i])

tmpFile=[]
replaced = False

with open('/home/samuel/eso121-g6_in_first_input.def','r') as f:
    data = f.readlines()
    f.close()
    
with open('/home/samuel/eso121-g6_in_first_input.def','a') as f:
    for i in data:
        if data.index(i)==38:
            pass
        lineVal = i.split()
        print("lineVal: ",lineVal)
        for j in lineVal:
            print("j @: ",j)
            if j == "VROT=":
                txt = "    VROT="+txt+"\n"
                tmpFile.append(txt)
                replaced = True
                break
            else:
                if lineVal.index(j)==len(lineVal)-1:
                    tmpFile.append(i)

#    print (tmpFile[26],tmpFile[27],tmpFile[28],tmpFile[29],tmpFile[30])    
    if replaced:
        f.seek(0)
        f.truncate()
        for i in tmpFile:
            f.write(i)
        f.close()
    data = fetchDefVals.getData('/home/samuel/software/TiRiFiC/tirific_2.3.4/tirific_example/eso121-g6_in_first_input.def')
    VROTvals = fetchDefVals.getParameter("VROT=",data)
    RADIvals = fetchDefVals.getParameter("RADI=",data)
    xList = RADIvals[:]
    yList = VROTvals*len(RADIvals)

    a.clear()
    a.plot(xList, yList)

    
            

class LiveGraph(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "Live Graph")
    
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container,self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

def getPoint(event):
    return (event.ydata)

    
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        canvas = FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        #canvas.mpl_connect('motion_notify_event',getPoint)
        
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def returnPoint(self,event):
        self.canvas.mpl_connect('motion_notify_event',getPoint)
        return (event.ydata)

app = LiveGraph()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()