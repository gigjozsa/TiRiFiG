# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file for the Tk implementation of TiRiFiG

"""


#import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk,sys,os
from math import ceil as mCeil
from tkinter import filedialog,Entry,StringVar
import subprocess as sp
#from matplotlib import pyplot as plt


class fetchDefVals:
    precisionPAR = 1
    precisionRADI = 1 
    
    def getData(filePath):
        with open(filePath) as f:
            data = f.readlines()
        f.close()
        return data
        
    def getParameter(sKey,data):
        global NUR
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
            if not(sKey=="NUR"):
                fetchDefVals.numPrecision(sKey,parVal)
            if not(sKey == "RADI"):
                precision = fetchDefVals.precisionPAR
            else:
                precision = fetchDefVals.precisionRADI
                
            for i in range(len(parVal)):
                parVal[i]=round(float(parVal[i]),precision)
            return parVal   
        else:
            zeroValues = []
            for i in range(int(NUR[0])):
                zeroValues.append(0.0)
            fetchDefVals.precisionPAR = 1
            return zeroValues
#            print("Search key not found")
        
    def numPrecision(sKey,data):
        decPoints = []
        
        for i in range(len(data)):
            val = data[i].split(".")
            #make sure val has two elements
            if len(val)==2:
                decPoints.append(len(val[1]))
        
        if not(sKey == "RADI"):
            if len(decPoints)==0:
                fetchDefVals.precisionPAR = 0
            else:
                fetchDefVals.precisionPAR = max(decPoints)
        else:
            if len(decPoints)==0:
                fetchDefVals.precisionRADI = 0
            else:
                fetchDefVals.precisionRADI = max(decPoints)
            
        #return max(decPoints)


def animate(i):
    global xScale,yScale,f,a,mPress,mRelease,mMotion,historyList,parVals,key,par,unitMeas
    
    if key=="Yes":
        a.clear()
        for ax in f.get_axes():
            ax.set_xlabel("RADI (arcsec)")
            ax.set_ylabel(par + "( "+unitMeas+ " )")
        #print(historyList[par][len(historyList[par])-1])
        a.plot(parVals['RADI'], historyList[par][len(historyList[par])-1],'--bo')
        a.set_xlim(xScale[0],xScale[1])            
        a.set_ylim(yScale[0],yScale[1]) 
        key = "No"
    
    for j in range(len(parVals['RADI'])):
        if (mPress[0] < (parVals['RADI'][j])+3) and (mPress[0] > (parVals['RADI'][j])-3) and (mRelease[0]=="None"):
            parVals[par][j] = mMotion[0]
            #print("historyList in motion: ",historyList)
            a.clear()
            for ax in f.get_axes():
                ax.set_xlabel("RADI (arcsec)")
                ax.set_ylabel(par + "( "+unitMeas+ " )")
            a.plot(parVals['RADI'], parVals[par],'--bo')
#            print("mMotion:",mMotion," yScale:",yScale)
            if (yScale[1] - mMotion[0])<=50:
                yScale[1] += 50
            elif (mMotion[0] - yScale[0])<= 50:
                yScale[0] -= 50
            a.set_xlim(xScale[0],xScale[1])            
            a.set_ylim(yScale[0],yScale[1])
    
    #print ("\nhistoryList: ",historyList)
            
                
class fMenu:
    
    def openFile():
        global fileName,data,VROT,RADI,historyList,xScale,yScale,key,numPrecisionY,numPrecisionX,app,par,NUR,parVals
        
        root = tk.Tk()
        root.withdraw()
        
        fileName = filedialog.askopenfilename(filetypes = (("first_input",".def"),("All files","*.*")))
        root.destroy()
        
        key = "Yes"
        
        
        if (not(fileName==None) and not(len(fileName)==0)):
            data = fetchDefVals.getData(fileName)
            VROT = fetchDefVals.getParameter("VROT",data)
            RADI = fetchDefVals.getParameter("RADI",data)
            numPrecisionY = fetchDefVals.precisionPAR
            numPrecisionX = fetchDefVals.precisionRADI
            #ensure there are the same points for VROT as there are for RADI as specified in NUR parameter
            NUR = fetchDefVals.getParameter("NUR",data)
            diff = NUR[0]-len(VROT)
            lastIndexItem = len(VROT)-1
            if diff == NUR[0]:
                for i in range(int(diff)):
                    VROT.append(0.0)
            elif diff > 0 and diff < NUR[0]:
                for i in range(int(diff)):
                    VROT.append(VROT[lastIndexItem])
            
            parVals = {'RADI':RADI[:],'VROT':VROT[:]}
            
            historyList.clear()
            historyList[par] = [VROT[:]]
            if (max(RADI)-min(RADI))<=100:
                xScale = [int(mCeil(-2*max(RADI))),int(mCeil(2*max(RADI)))]                           
            else:
                xScale = [int(mCeil(min(RADI)-0.1*(max(RADI)-min(RADI)))),int(mCeil(max(RADI)+0.1*(max(RADI)-min(RADI))))]                            
                #print ('@if: ',len(VROTvals))
            if (max(VROT)-min(VROT))<=100:
                yScale = [int(mCeil(-2*max(VROT))),int(mCeil(2*max(VROT)))]
            else:
                yScale = [int(mCeil(min(VROT)-0.1*(max(VROT)-min(VROT)))),int(mCeil(max(VROT)+0.1*(max(VROT)-min(VROT))))]
                #print ('@if: ',len(VROTvals))
        else:
            global app
            if len(VROT)==0:
                sys.exit(0)
         

                
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
        global data,numPrecisionY,numPrecisionX
        
        if sKey == 'RADI':
            r = numPrecisionX
        else:
            r = numPrecisionY
            
        #get the new values and format it as [0 20 30 40 50...]
        txt =""
        for i in range(len(newVals)):
            txt = txt+" " +'{0:.{1}f}'.format(newVals[i], r)

            #txt = txt+" " + str(newVals[i])

        tmpFile=[]
        with open(filePath,'a') as f:
            status = False
            for i in data:
                lineVals = i.split("=")
                if (len(lineVals)>1):
                    lineVals[0]=''.join(lineVals[0].split())
                    if (sKey == lineVals[0]):
                        txt = "    "+sKey+"="+txt+"\n"
                        tmpFile.append(txt)
                        status = True
                    else:
                        tmpFile.append(i)
                else:
                    tmpFile.append(i)
     
            
            if not(status):
                tmpFile.append("# "+par+" parameter in "+unitMeas+"\n")
                txt = "    "+sKey+"="+txt+"\n"
                tmpFile.append(txt)
                
            f.seek(0)
            f.truncate()
            for i in tmpFile:
                f.write(i)
            
            data = tmpFile[:]
            f.close()
        
    
    def saveAll():
        for i in parVals:
            fMenu.saveFile(parVals[i],i,fileName)
        fMenu.saveMsg()
                
    def saveAs(filename,newVals,sKey):
        global data,numPrecisionY,numPrecisionX
        
        if sKey == 'RADI':
            r = numPrecisionX
        else:
            r = numPrecisionY
        
        #get the new values and format it as [0 20 30 40 50...]
        txt =""
        for i in range(len(newVals)):
            txt = txt+" " +'{0:.{1}f}'.format(newVals[i], r)
            #txt = txt+" " + str(newVals[i])
            
        tmpFile=[]
        
        if not(fileName==None):
            status = False
            for i in data:
                lineVals = i.split("=")
                if (len(lineVals)>1):
                    lineVals[0]=''.join(lineVals[0].split())
                    if (sKey == lineVals[0]):
                        txt = "    "+sKey+"="+txt+"\n"
                        tmpFile.append(txt)
                        status = True
                    else:
                        tmpFile.append(i)
                else:
                    tmpFile.append(i)
         
            if not(status):
                tmpFile.append("# "+par+" parameter in "+unitMeas+"\n")
                txt = "    "+sKey+"="+txt+"\n"
                tmpFile.append(txt)
            
            fileName.seek(0)
            fileName.truncate()
            for i in tmpFile:
                fileName.write(i)
                
            data = tmpFile[:]
            fileName.close()

    def saveAsAll():
        root = tk.Tk()
        root.withdraw()
        fileName = filedialog.asksaveasfile(mode='w', defaultextension=".def",filetypes = (("TiRiFiC default file",".def"),("All files","*.*")))
        root.destroy()
        for i in parVals:
            fMenu.saveAs(fileName,parVals[i],i)
        fMenu.saveMsg()
    
    
    def startTerrific():
        global fileName
#        os.system("gnome-terminal -e echo blah;sleep 10")
#        os.system("gnome-terminal -e 'bash -c \"pwd; exec bash\"'")
        os.system("gnome-terminal -e 'bash -c \"/home/samuel/software/TiRiFiC/tirific_2.3.4/bin/tirific deffile = "+fileName+"; exec bash\"'")
        
    def exitApp():
        global app,f,a,mPress,mRelease,mMotion,historyList,xScale,yScale,fileName,key,data,VROT,RADI,par,unitMeas,numPrecisionY,numPrecisionX,parVals
        
        del f,a,mPress,mRelease,mMotion,historyList,xScale,yScale,fileName,key,data,VROT,RADI,par,unitMeas,numPrecisionY,numPrecisionX,parVals
        app.destroy()


class eMenu:
    
    def openEditor():
        def center(w,h):
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = screen_width/2 - w/2
            y = screen_height/2 - h/2
            root.geometry("%dx%d+%d+%d" % (w,h,x, y))
        root = tk.Tk()
        root.wm_title("Open Editor")
        center(190,115)
        
        def opentxtFile():
            global fileName

            if len(txtEditor.get())>0:
                programName = str(txtEditor.get())
                os.system("gnome-terminal -e 'bash -c \""+programName+" "+fileName+"; exec bash\"'")
            else:
                os.system("gnome-terminal -e 'bash -c \"gedit "+fileName+"; exec bash\"'")
                
            root.destroy()        
        
        labelEmpty1 = tk.Label(root,text ="e.g. vi, emacs, gedit, subl...",font=SMALL_FONT)
        labelEmpty1.grid(sticky='e')
        
        labelEmpty1 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty1.grid(sticky='e')
    
        labelEditor = tk.Label(root,text ="",font=SMALL_FONT)
        labelEditor.grid(sticky='w')
        
        defEditor = StringVar(root,value="gedit")
        txtEditor = Entry(root,textvariable=defEditor)
        txtEditor.grid(row=2, column=0)
        txtEditor.focus_set() 
        
        labelEditor = tk.Label(root,text ="",font=SMALL_FONT)
        labelEditor.grid(sticky='w')   
        
        B1 = tk.Button(root,text = "Open File", command = lambda: opentxtFile())
        B1.grid(row=4, column=0,sticky='w') 
    
    def graphScale():
        global yScale,xScale,par
        
        def center(w,h):
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = screen_width/2 - w/2
            y = screen_height/2 - h/2
            root.geometry("%dx%d+%d+%d" % (w,h,x, y))
        
        def updateYScale():
            global key,numPrecisionY,numPrecisionX
            key = "Yes"
#            if len(yMin.get())>0:
#                if float(yMin.get())<=min(VROTvals):
#                    yScale[0] = float(defMin.get())
#            if len(yMax.get())>0:
#                if float(yMax.get())>=max(VROTvals):
#                    yScale[1] = float(defMax.get())
            if len(yMin.get())>0:
                yScale[0] = int(mCeil(float(yMin.get())))
            if len(yMax.get())>0:
                yScale[1] = int(mCeil(float(yMax.get())))
            if len(xMin.get())>0:
                xScale[0] = int(mCeil(float(xMin.get())))
            if len(xMax.get())>0:
                xScale[1] = int(mCeil(float(xMax.get())))
            root.destroy()
            
        root = tk.Tk()
        root.wm_title("Axis Scale")
        center(250,180)
        
         
        labelEmpty1 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty1.grid(sticky='e')
    
        labelyMin = tk.Label(root,text =par+" min",font=SMALL_FONT)
        labelyMin.grid(sticky='w')
        
        defyMin = StringVar(root,value='{0:.{1}f}'.format(yScale[0], numPrecisionY))
        yMin = Entry(root,textvariable=defyMin)
        yMin.grid(row=1, column=1)
        yMin.focus_set()     

        labelEmpty2 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty2.grid(sticky='e')
               
        labelyMax = tk.Label(root,text =par+" max",font=SMALL_FONT)
        labelyMax.grid(sticky='w')
        defyMax = StringVar(root,value='{0:.{1}f}'.format(yScale[1], numPrecisionY))        
        yMax = Entry(root,textvariable=defyMax)
        yMax.grid(row=3, column=1)
        
        
        ############################################################
        
        labelEmpty3 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty3.grid(sticky='e')
    
        labelxMin = tk.Label(root,text ="RADI min",font=SMALL_FONT)
        labelxMin.grid(sticky='w')
        defxMin = StringVar(root,value='{0:.{1}f}'.format(xScale[0], numPrecisionX))
        xMin = Entry(root,textvariable=defxMin)
        xMin.grid(row=5, column=1)
        xMin.focus_set()     

        labelEmpty4 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty4.grid(sticky='e')
               
        labelxMax = tk.Label(root,text ="RADI max",font=SMALL_FONT)
        labelxMax.grid(sticky='w')
        defxMax = StringVar(root,value='{0:.{1}f}'.format(xScale[1], numPrecisionX))        
        xMax = Entry(root,textvariable=defxMax)
        xMax.grid(row=7, column=1)
        
        ############################################################
        
        B1 = tk.Button(root,text = "OK", command = lambda: updateYScale())
        B1.grid(row=8, column=0) 
            
    def setPrecision():
        
        global numPrecisionX,numPrecisionY,RADI,VROT,par
        
        def center(w,h):
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = screen_width/2 - w/2
            y = screen_height/2 - h/2
            root.geometry("%dx%d+%d+%d" % (w,h,x, y))
        
        def updatePrecision():
            global numPrecisionX,numPrecisionY
            if len(yAxis.get())>0 and float(yAxis.get())>=0:
                numPrecisionY = int(yAxis.get())
                for i in range(len(parVals[par])):
                    parVals[par][i] = round(parVals[par][i],int(yAxis.get()))
            
            if len(xAxis.get())>0 and float(xAxis.get())>=0:
                numPrecisionX = int(xAxis.get())
                for i in range(len(parVals['RADI'])):
                    parVals['RADI'][i] = round(parVals['RADI'][i],int(xAxis.get()))
                
            root.destroy()
        
        root = tk.Tk()
        root.wm_title("Precision")
        center(250,110)
        
        labelEmpty1 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty1.grid(sticky='e')
        
        
        xLabel = tk.Label(root,text ="RADI d.p",font=SMALL_FONT)
        xLabel.grid(sticky='w')
        defxAxis = StringVar(root,value=numPrecisionX)        
        xAxis = Entry(root,textvariable=defxAxis)
        xAxis.grid(row=1, column=1)
        xAxis.focus_set()
        
        labelEmpty2 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty2.grid(sticky='e')
        
        
        yLabel = tk.Label(root,text =par+" d.p",font=SMALL_FONT)
        yLabel.grid(sticky='w')
        defyAxis = StringVar(root,value=numPrecisionY) 
        yAxis = Entry(root,textvariable=defyAxis)
        yAxis.grid(row=3, column=1)
        
        B1 = tk.Button(root,text = "OK", command = lambda: updatePrecision())
        B1.grid(row=4, column=0)
        
        #######################################################################
    def setParameter():
        
        global data,parVals,yScale,key,par,unitMeas
        
        def center(w,h):
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = screen_width/2 - w/2
            y = screen_height/2 - h/2
            root.geometry("%dx%d+%d+%d" % (w,h,x, y))
        
        def updateParameter():
            global data,parVals,yScale,key,par,unitMeas,numPrecisionY,NUR
            
            if len(parameterVal.get())>0 and not(str(parameterVal.get())==par):
                par = str(parameterVal.get())
#                print("par: ",par)
                unitMeas = str(unitMeasurement.get())
            
                exec(par + "= fetchDefVals.getParameter(par,data)") in globals(), locals()
                
                numPrecisionY = fetchDefVals.precisionPAR
                
                #ensure there are the same points for PAR as there are for RADI as specified in NUR parameter
                #NUR = fetchDefVals.getParameter("NUR",data)
                tmp = eval(par)
                diff = NUR[0]-len(tmp)
                lastIndexItem = len(tmp)-1
                if diff == NUR[0]:
                    for i in range(int(diff)):
                        eval(par).append(0.0)
                elif diff > 0 and diff < NUR[0]:
                    for i in range(int(diff)):
                        eval(par).append(tmp[lastIndexItem])
                
                parVals[par] = eval(par)
                
                historyList[par] = [parVals[par][:]]
                
                #print (historyList)
                if max(parVals[par])<=0:
                    yScale = [-50,50]
                elif (max(parVals[par])-min(parVals[par]))<=100:
                    yScale = [int(mCeil(-2*max(parVals[par]))),int(mCeil(2*max(parVals[par])))]
                else:
                    yScale = [int(mCeil(min(parVals[par])-0.1*(max(parVals[par])-min(parVals[par])))),int(mCeil(max(parVals[par])+0.1*(max(parVals[par])-min(parVals[par]))))]
                
                key = "Yes"
                
                root.destroy()            
                
                
            
        
        root = tk.Tk()
        root.wm_title("Parameter")
        center(250,110)
        
        labelEmpty1 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty1.grid(sticky='e')
        
        #create a variable to store default parameter and default measurement
        
        parValLabel = tk.Label(root,text ="Parameter",font=SMALL_FONT)
        parValLabel.grid(sticky='e')
        defParameter = StringVar(root,value=par)        
        parameterVal = Entry(root,textvariable=defParameter)
        parameterVal.grid(row=1, column=1)
        parameterVal.focus_set()
        
        labelEmpty2 = tk.Label(root,text ="",font=SMALL_FONT)
        labelEmpty2.grid(sticky='e')
        
        
        unitMeasLabel = tk.Label(root,text ="Unit",font=SMALL_FONT)
        unitMeasLabel.grid(sticky='w')
        defMeas = StringVar(root,value="km/s") 
        unitMeasurement = Entry(root,textvariable=defMeas)
        unitMeasurement.grid(row=3, column=1)
        
        B1 = tk.Button(root,text = "OK", command = lambda: updateParameter())
        B1.grid(row=4, column=0) 
        #######################################################################
    


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
                             command=lambda: fMenu.saveAll())
        fileMenu.add_separator()                     
        fileMenu.add_command(label="Save as",
                             command=lambda: fMenu.saveAsAll())
        fileMenu.add_separator()
        fileMenu.add_command(label="Start",
                             command=lambda: fMenu.startTerrific())
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit",
                             command=lambda: fMenu.exitApp())
                             
        menubar.add_cascade(label="File",menu=fileMenu)
        
        
        
        editMenu = tk.Menu(menubar, tearoff = 0)
        editMenu.add_command(label="Scale Manager",
                             command=lambda: eMenu.graphScale())
        editMenu.add_separator()
        editMenu.add_command(label="Precision",
                             command=lambda: eMenu.setPrecision())
        editMenu.add_separator()
        editMenu.add_command(label="Open in Editor",
                             command=lambda: eMenu.openEditor())
        editMenu.add_separator()
        editMenu.add_command(label="Parameter",
                             command=lambda: eMenu.setParameter())
                             
        menubar.add_cascade(label="Edit",menu=editMenu)
                    
        
        tk.Tk.config(self, menu=menubar)
        
        
        self.frames = {}

        frame = StartPage(container,self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        
        
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        

class Events:
    global numPrecisionY,historyList,par,RADI,mMotion,mPress,mRelease
    def getClick(event):
        global numPrecisionY,historyList,par,RADI,mMotion,mPress,mRelease
        if event.xdata == None:
            pass
        else:
            mPress[0]=round(float(event.xdata),numPrecisionY)
            mRelease[0]="None"
            
    def getRelease(event):
        global numPrecisionY,historyList,par,RADI,mMotion,mPress,mRelease
        if not(event.ydata == None):
            mRelease[0]=round(float(event.ydata),numPrecisionY)
            if not(historyList[par][len(historyList[par])-1]==parVals[par][:]):
                historyList[par].append(parVals[par][:])
                mPress[0]=-5+min(RADI)
                mRelease[0]="None"
    
    def getMotion(event):
        global numPrecisionY,historyList,par,RADI,mMotion,mPress,mRelease
        if event.ydata == None:
            pass
        else:
            mMotion[0]=round(float(event.ydata),numPrecisionY)
    
    def keyPressed(event):
        global numPrecisionY,historyList,par,RADI,mMotion,mPress,mRelease
        global key
        if event.key == "ctrl+z" or event.key == "ctrl+Z":
            if len(historyList[par])>1:
                historyList[par].pop()
            #print('historyList after undo: ',historyList)
            tempHistoryList = historyList[par][len(historyList[par])-1]
            for i in range(len(parVals[par])):
                parVals[par][i]=round(tempHistoryList[i],numPrecisionY) 
            key = "Yes"

    
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

historyList={}
xScale=[0,0]
yScale=[0,0]
fileName = None
key = "Yes"

NUR = [0]
data=[]
VROT=[]
RADI=[]
par = 'VROT'
unitMeas = 'km/s'
numPrecisionY = 0
numPrecisionX = 0
fMenu.openFile()
mPress=[-5+min(RADI)];mRelease=['None'];mMotion=[-5+min(RADI)]


parVals = {'RADI':RADI[:],'VROT':VROT[:]}

app = LiveGraph()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=500)
app.mainloop()
