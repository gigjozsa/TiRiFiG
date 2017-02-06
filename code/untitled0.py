# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:12:17 2016

@author: samuel
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 01:09:38 2016

@author: samuel
"""

#import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(7,7), dpi=100)
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
            parVal[i]=float(parVal[i])
        return parVal        


#canvas.mpl_connect('motion_notify_event',getPoint)


    
def animate(i):
    
    data = fetchDefVals.getData('/home/samuel/software/TiRiFiC/tirific_2.3.4/tirific_example/eso121-g6_in_first_input.def')
    VROTvals = fetchDefVals.getParameter("VROT=",data)
    RADIvals = fetchDefVals.getParameter("RADI=",data)
    xList = RADIvals[:]
    yList = VROTvals*len(RADIvals)

    a.clear()
    
    for ax in f.get_axes():
        ax.set_xlabel("RADI (arcsec)")
        ax.set_ylabel("VROT(km/s)")

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
    return event.ydata
    
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Viewgraph VROT (rotation velocity) vs RADI", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.canvasPlot()
    
    def canvasPlot(self):
        canvas = FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        return canvas.mpl_connect('motion_notify_event',getPoint)
     


app = LiveGraph()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()