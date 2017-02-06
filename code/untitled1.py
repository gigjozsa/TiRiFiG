## -*- coding: utf-8 -*-
#"""
#Created on Mon Sep  5 13:48:34 2016
#
#@author: samuel
#"""
##import matplotlib
##matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
#import matplotlib.animation as animation
#from matplotlib import style
#import tkinter as tk
#from tkinter import ttk
##from matplotlib import pyplot as plt
#
#class fetchDefVals:
#    
#    def getData(filePath):
#        with open(filePath) as f:
#            data = f.readlines()
#        f.close()
#        return data
#        
#    def getParameter(sKey,data):
#        status = False
#        for i in data:
#            lineVals = i.split("=")
#            if (len(lineVals)>1):
#                lineVals[0]=''.join(lineVals[0].split())
#                if (sKey == lineVals[0]):
#                    parVal = lineVals[1].split()
#                    status = True
#                    break
#        if status:        
#            for i in range(len(parVal)):
#                parVal[i]=float(parVal[i])
#            return parVal   
#        else:
#            print("Search key not found")
#
#
#def animate(i):
#
#    for j in range(len(RADIvals)):
#        if (mPress[0] < RADIvals[j]+0.5) and (mPress[0] > RADIvals[j]-0.5) and (mRelease[0]=="None"):
#            VROTvals[j] = mMotion[0]
#            a.clear()
#            for ax in f.get_axes():
#                ax.set_xlabel("RADI (arcsec)")
#                ax.set_ylabel("VROT(km/s)")
#            a.plot(RADIvals, VROTvals,'--bo')
#            #a.get_yaxis().get_major_formatter().set_useOffset(False)
#            a.set_xlim(-20,250)            
#            a.set_ylim(0,500)
#            
#def saveMsg():
#    popup = tk.Tk()
#    popup.wm_title("Information")
#    #popup.pack()
#    
#    label = ttk.Label(popup,text ="Successful!",font=LARGE_FONT)
#    label.pack(side = "top", fill = "x",padx = 10,pady = 10)
#    B1 = ttk.Button(popup,text = "OK", command = popup.destroy())
#    B1.pack()   
#    
#def saveFile(newVals,sKey,filePath):  
#    
#    #get the new values and format it as [0 20 30 40 50...]
#    txt =""
#    for i in range(len(newVals)):
#        txt = txt+" " + str(newVals[i])
#        
#    tmpFile=[]
#    with open(filePath,'a') as f:
#        for i in data:
#            lineVals = i.split("=")
#            if (len(lineVals)>1):
#                lineVals[0]=''.join(lineVals[0].split())
#                if (sKey == lineVals[0]):
#                    txt = "    "+sKey+"="+txt+"\n"
#                    tmpFile.append(txt)
#                else:
#                    tmpFile.append(i)
#            else:
#                tmpFile.append(i)
# 
#        f.seek(0)
#        f.truncate()
#        for i in tmpFile:
#            f.write(i)
#        f.close()
#    #saveMsg()
#            
#class LiveGraph(tk.Tk):
#
#    def __init__(self, *args, **kwargs):
#        
#        tk.Tk.__init__(self, *args, **kwargs)
#        
#        tk.Tk.wm_title(self, "Live Graph")
#    
#        container = tk.Frame(self)
#        container.pack(side="top", fill="both", expand = True)
#        container.grid_rowconfigure(0, weight=1)
#        container.grid_columnconfigure(0, weight=1)
#        
#        menubar = tk.Menu(container)
#        fileMenu = tk.Menu(menubar, tearoff = 0)
#        fileMenu.add_command(label="Save Changes",
#                             command=lambda: saveFile(VROTvals,"VROT",'/home/samuel/eso121-g6_in_first_input.def'))
#        fileMenu.add_separator()
#        #fileMenu.add_command(label="Exit",command= tk.Tk.quit(container))
#        menubar.add_cascade(label="File",menu=fileMenu)
#        tk.Tk.config(self, menu=menubar)
#
#        self.frames = {}
#
#        frame = StartPage(container,self)
#        self.frames[StartPage] = frame
#        frame.grid(row=0, column=0, sticky="nsew")
#        self.show_frame(StartPage)
#        
#        
#    def show_frame(self, cont):
#
#        frame = self.frames[cont]
#        frame.tkraise()
#
#class mouseEvents:
#    def getClick(event):
#        if event.xdata == None:
#            pass
#        else:
#            mPress[0]=round(float(event.xdata),1)
#            mRelease[0]="None"
#            
#    def getRelease(event):
#        mRelease[0]=round(float(event.ydata),1)
#    
#    def getMotion(event):
#        if event.ydata == None:
#            pass
#        else:
#            mMotion[0]=round(float(event.ydata),1)
#    
#class StartPage(tk.Frame):
#
#    def __init__(self, parent, controller):
#        tk.Frame.__init__(self, parent)
#        label = tk.Label(self, text="Viewgraph VROT (rotation velocity) vs RADI", font=LARGE_FONT)
#        label.pack(pady=10,padx=10)
#        
##        button = ttk.Button(self, text="Save Changes",
##                            command=lambda: saveFile(VROTvals,"VROT",'/home/samuel/eso121-g6_in_first_input.def'))
##        button.pack()
#        
#        canvas = FigureCanvasTkAgg(f,self)
#        canvas.show()
#        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
#        
#        canvas.mpl_connect('button_press_event', mouseEvents.getClick)
#        canvas.mpl_connect('button_release_event', mouseEvents.getRelease)
#        canvas.mpl_connect('motion_notify_event', mouseEvents.getMotion)
#        
#        toolbar = NavigationToolbar2TkAgg(canvas, self)
#        toolbar.update()
#        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#        
#
#
##global variables
#     
#LARGE_FONT= ("Verdana", 12)
#style.use("ggplot")
#
##f = Figure(figsize=(10,5), dpi=100)
#f = Figure()
#a = f.add_subplot(111)
#
#mPress=[-1];mRelease=["None"];mMotion=[-1]
#historyList=[]
#
#data = fetchDefVals.getData('/home/samuel/eso121-g6_in_first_input.def')
#VROTvals = fetchDefVals.getParameter("VROT",data)
#RADIvals = fetchDefVals.getParameter("RADI",data)
#
##ensure there are the same points for VROT as there are for RADI as specified in NUR parameter
#NUR = fetchDefVals.getParameter("NUR",data)
#diff = NUR[0]-len(VROTvals)
#lastItemIndex = len(VROTvals)-1
#if diff == NUR[0]:
#    for i in range(int(diff)):
#        VROTvals.append(0.0)
#elif diff > 0 and diff < NUR[0]:
#    for i in range(int(diff)):
#        VROTvals.append(VROTvals[lastItemIndex])
#
##initial graph before changes are made    
#for ax in f.get_axes():
#    ax.set_xlabel("RADI (arcsec)")
#    ax.set_ylabel("VROT(km/s)")
#a.plot(RADIvals, VROTvals,linestyle='--', marker='o', color='b') 
##a.get_yaxis().get_major_formatter().set_useOffset(False)
#a.set_ylim(0,500)
#a.set_xlim(-20,250)
#
#app = LiveGraph()
#app.geometry("1280x720")
#ani = animation.FuncAnimation(f, animate, interval=200)
#app.mainloop()
#


# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


#import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import filedialog,Entry,StringVar
#from matplotlib import pyplot as plt


class fetchDefVals:
    
    def getData(filePath):
        with open(filePath) as f:
            data = f.readlines()
        f.close()
        return data
        
    def getParameter(sKey,data):
        status = False
        for i in data:
            lineVals = i.split("=")
            if (len(lineVals)>1):
                lineVals[0]=''.join(lineVals[0].split())
                if (sKey == lineVals[0]):
                    parVal = lineVals[1].split()
                    status = True
                    break
        if status:        
            for i in range(len(parVal)):
                parVal[i]=float(parVal[i])
            return parVal   
        else:
            print("Search key not found")


def animate(i):
    ##global xScale,yScale
    for j in range(len(RADIvals)):
        if (mPress[0] < RADIvals[j]+1) and (mPress[0] > RADIvals[j]-1) and (mRelease[0]=="None"):
            VROTvals[j] = mMotion[0]
            a.clear()
            for ax in f.get_axes():
                ax.set_xlabel("RADI (arcsec)")
                ax.set_ylabel("VROT(km/s)")
            a.plot(RADIvals, VROTvals,'--bo')
            a.set_xlim(xScale[0],xScale[1])            
            a.set_ylim(yScale[0],yScale[1])
        else:
            a.clear()
            for ax in f.get_axes():
                ax.set_xlabel("RADI (arcsec)")
                ax.set_ylabel("VROT(km/s)")
            a.plot(RADIvals, historyList[len(historyList)-1],'--bo')
            a.set_xlim(xScale[0],xScale[1])            
            a.set_ylim(yScale[0],yScale[1])
    #print ("\nhistoryList: ",historyList)
            
                
class fMenu:
    
    
    def openFile():
        root = tk.Tk()
        root.withdraw()
        global fileName 
        fileName = filedialog.askopenfilename(filetypes = (("first_input",".def"),("All files","*.*")))
        root.destroy()
        
        global data,VROTvals,RADIvals,historyList,xScale,yScale
        
        
        
        if (not(fileName==None) and not(len(fileName)==0)):
            data = fetchDefVals.getData(fileName)
            VROTvals = fetchDefVals.getParameter("VROT",data)
            RADIvals = fetchDefVals.getParameter("RADI",data)
            
            #ensure there are the same points for VROT as there are for RADI as specified in NUR parameter
            NUR = fetchDefVals.getParameter("NUR",data)
            diff = NUR[0]-len(VROTvals)
            lastIndexItem = len(VROTvals)-1
            if diff == NUR[0]:
                for i in range(int(diff)):
                    VROTvals.append(0.0)
            elif diff > 0 and diff < NUR[0]:
                for i in range(int(diff)):
                    VROTvals.append(VROTvals[lastIndexItem])
            
            historyList = []
            historyList.append(VROTvals[:])
            xScale = [min(RADIvals)-10,max(RADIvals)+10]
            yScale = [min(VROTvals)-2*min(VROTvals),max(VROTvals)+min(VROTvals)*2]
            #print ('@if: ',len(VROTvals))
        else:
            #print ('@else: ',len(VROTvals))
            if len(VROTvals)==0:
                for i in range(11):
                    RADIvals.append(i*10)
                    VROTvals.append(0)
                #print ('@fter else: ',len(VROTvals))
                historyList.append(VROTvals[:])
                xScale = [RADIvals[0]-10,RADIvals[10]+10]
                yScale = [0,300]
        
                
    def saveMsg():
        
        def center(w,h):
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            x = screen_width/2 - w/2
            y = screen_height/2 - h/2
            popup.geometry("%dx%d+%d+%d" % (w,h,x, y))
        
        
        popup = tk.Tk()
        popup.wm_title("Information")
        center(165,65)
        
        label = tk.Label(popup,text ="Successful!",font=LARGE_FONT)
        #label.pack(pady=10,padx=10)
        label.pack(side = "top", fill = "x",padx = 10,pady = 10)
        B1 = tk.Button(popup,text = "OK", command = lambda: popup.destroy())
        B1.pack()      
    
    def saveFile(newVals,sKey,filePath):  
        
        #get the new values and format it as [0 20 30 40 50...]
        txt =""
        for i in range(len(newVals)):
            txt = txt+" " + str(newVals[i])
            
        tmpFile=[]
        with open(filePath,'a') as f:
            for i in data:
                lineVals = i.split("=")
                if (len(lineVals)>1):
                    lineVals[0]=''.join(lineVals[0].split())
                    if (sKey == lineVals[0]):
                        txt = "    "+sKey+"="+txt+"\n"
                        tmpFile.append(txt)
                    else:
                        tmpFile.append(i)
                else:
                    tmpFile.append(i)
     
            f.seek(0)
            f.truncate()
            for i in tmpFile:
                f.write(i)
            f.close()
        fMenu.saveMsg()
                
    def saveAs(newVals,sKey):  
        
        #get the new values and format it as [0 20 30 40 50...]
        txt =""
        for i in range(len(newVals)):
            txt = txt+" " + str(newVals[i])
            
        tmpFile=[]
        root = tk.Tk()
        root.withdraw()
        fileName = filedialog.asksaveasfile(mode='w', defaultextension=".def",filetypes = (("TiRiFiC default file",".def"),("All files","*.*")))
        root.destroy()
        if not(fileName==None):
            for i in data:
                lineVals = i.split("=")
                if (len(lineVals)>1):
                    lineVals[0]=''.join(lineVals[0].split())
                    if (sKey == lineVals[0]):
                        txt = "    "+sKey+"="+txt+"\n"
                        tmpFile.append(txt)
                    else:
                        tmpFile.append(i)
                else:
                    tmpFile.append(i)
         
            fileName.seek(0)
            fileName.truncate()
            for i in tmpFile:
                fileName.write(i)
            fileName.close()
            fMenu.saveMsg()            
    
    def exitApp():
        global app
        
        app.destroy()


class eMenu:
    
    def VROTscale():
        global yScale
        def center(w,h):
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = screen_width/2 - w/2
            y = screen_height/2 - h/2
            root.geometry("%dx%d+%d+%d" % (w,h,x, y))
        
        def updateYScale():
            global VROTvals
#            if len(yMin.get())>0:
#                if float(yMin.get())<=min(VROTvals):
#                    yScale[0] = float(defMin.get())
#            if len(yMax.get())>0:
#                if float(yMax.get())>=max(VROTvals):
#                    yScale[1] = float(defMax.get())
            if len(yMin.get())>0:
                yScale[0] = float(yMin.get())
            if len(yMax.get())>0:
                yScale[1] = float(yMax.get())
            root.destroy()
            
        root = tk.Tk()
        root.wm_title("Vertical Axis Scale")
        center(250,110)
        
         
        labelEmpty1 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty1.grid(sticky='e')
    
        labelMin = tk.Label(root,text ="VROT min",font=SMALL_FONT)
        labelMin.grid(sticky='e')
        
        defMin = StringVar(root,value=yScale[0])
                
        yMin = Entry(root,textvariable=defMin)
        yMin.grid(row=1, column=1)
        yMin.focus_set()     

        labelEmpty2 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty2.grid(sticky='e')
               
        labelMax = tk.Label(root,text ="VROT max",font=SMALL_FONT)
        labelMax.grid(sticky='e')
        
        defMax = StringVar(root,value=yScale[1])
        
        yMax = Entry(root,textvariable=defMax)
        yMax.grid(row=3, column=1)
        
        B1 = tk.Button(root,text = "OK", command = lambda: updateYScale())
        B1.grid(row=4, column=0) 
            
    def setPrecision():
        
        def center(w,h):
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = screen_width/2 - w/2
            y = screen_height/2 - h/2
            root.geometry("%dx%d+%d+%d" % (w,h,x, y))
        root = tk.Tk()
        root.wm_title("Vertical Axis Scale")
        center(250,110)
        
         
        labelEmpty1 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty1.grid(sticky='e')
        
        labelMin = tk.Label(root,text ="VROT min",font=SMALL_FONT)
        labelMin.grid(sticky='e')
        yMin = Entry(root)
        yMin.grid(row=1, column=1)
        yMin.focus_set()
        
        labelEmpty2 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty2.grid(sticky='e')
        
        
        labelMax = tk.Label(root,text ="VROT max",font=SMALL_FONT)
        labelMax.grid(sticky='e')
        yMax = Entry(root)
        yMax.grid(row=3, column=1)
        
#        B1 = tk.Button(root,text = "OK", command = lambda: updateYScale())
#        B1.grid(row=4, column=0) 
    
    


class LiveGraph(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "Live Graph")
    
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        fileMenu = tk.Menu(menubar, tearoff = 0)
        fileMenu.add_command(label="Open",
                             command=lambda: fMenu.openFile())
        fileMenu.add_separator()
        fileMenu.add_command(label="Save Changes",
                             command=lambda: fMenu.saveFile(VROTvals,"VROT",fileName))
        fileMenu.add_command(label="Save as",
                             command=lambda: fMenu.saveAs(VROTvals,"VROT"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Scale Manager",
                             command=lambda: eMenu.VROTscale())
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit",
                             command=lambda: fMenu.exitApp())
        
                             
        menubar.add_cascade(label="File",menu=fileMenu)
        
        tk.Tk.config(self, menu=menubar)
        
#        
#        menubar.add_cascade(label="File",menu=fileMenu)
#        
#        
#        
#        editMenu = tk.Menu(menubar, tearoff = 0)
#        editMenu.add_command(label="Scale Manager",
#                             command=lambda: editMenu.VROTscale())
#        editMenu.add_separator()
#        editMenu.add_command(label="Save Changes     Ctrl+S",
#                             command=lambda: editMenu.saveFile(VROTvals,"VROT",fileName))
#        editMenu.add_command(label="Save as...     Shift+Ctrl+S",
#                             command=lambda: editMenu.saveAs(VROTvals,"VROT"))
#        editMenu.add_separator()
#        editMenu.add_command(label="Exit",
#                             command=lambda: editMenu.exitApp())
        #menubar.add_cascade(label="Edit",menu=editMenu)
        

        self.frames = {}

        frame = StartPage(container,self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        
        
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        

class Events:
    def getClick(event):
        if event.xdata == None:
            pass
        else:
            mPress[0]=round(float(event.xdata),1)
            mRelease[0]="None"
            
    def getRelease(event):
        if not(event.ydata == None):
            mRelease[0]=round(float(event.ydata),1)
            if not(historyList[len(historyList)-1]==VROTvals[:]):
                historyList.append(VROTvals[:])
                mPress[0]=-1
                mRelease[0]="None"
    
    def getMotion(event):
        if event.ydata == None:
            pass
        else:
            mMotion[0]=round(float(event.ydata),1)
    
    def keyPressed(event):
        if event.key == "ctrl+z" or event.key == "ctrl+Z":
            if len(historyList)>1:
                historyList.pop()
            tempHistoryList = historyList[len(historyList)-1]
            for i in range(len(VROTvals)):
                VROTvals[i]=tempHistoryList[i]          
        

    
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Viewgraph VROT (rotation velocity) vs RADI", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
#        button = ttk.Button(self, text="Save Changes",
#                            command=lambda: saveFile(VROTvals,"VROT",'/home/samuel/eso121-g6_in_first_input.def'))
#        button.pack()
        
        canvas = FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        canvas.mpl_connect('button_press_event', Events.getClick)
        canvas.mpl_connect('button_release_event', Events.getRelease)
        canvas.mpl_connect('motion_notify_event', Events.getMotion)
        canvas.mpl_connect('key_press_event', Events.keyPressed)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        



#global variables
     
LARGE_FONT= ("Verdana", 12)
SMALL_FONT= ("Verdana", 9)
style.use("ggplot")

f = Figure()
a = f.add_subplot(111)

mPress=[-1];mRelease=["None"];mMotion=[-1]
historyList=[]
xScale=[]
yScale=[]
fileName = None


data=[]
VROTvals=[]
RADIvals=[]
fMenu.openFile()


app = LiveGraph()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=200)
app.mainloop()