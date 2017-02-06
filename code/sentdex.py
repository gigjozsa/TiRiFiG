# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 09:33:19 2017

@author: samuel
"""

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import sys
from math import ceil as mCeil
from PyQt4 import QtCore, QtGui


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

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        #self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

        exitAction = QtGui.QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip('Leave The App')
        exitAction.triggered.connect(fMenu.close_application)

#        openEditor = QtGui.QAction("&Editor", self)
#        openEditor.setShortcut("Ctrl+E")
#        openEditor.setStatusTip('Open Editor')
#        openEditor.triggered.connect(self.editor)

        openFile = QtGui.QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(fMenu.file_open)

        self.statusBar()

        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAction)
        
        
#        editorMenu = mainMenu.addMenu("&Editor")
#        editorMenu.addAction(openEditor)
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        self.canvas = FigureCanvasQTAgg(f)
        self.toolbar = NavigationToolbar2QT(self.canvas,self)
        grid.addWidget(self.canvas,2,0,1,2)
        grid.addWidget(self.toolbar,1,0,1,2)
        
#        canvas.show()
        
        self.canvas.mpl_connect('button_press_event', Events.getClick)
        self.canvas.mpl_connect('button_release_event', Events.getRelease)
        self.canvas.mpl_connect('motion_notify_event', Events.getMotion)
        self.canvas.mpl_connect('key_press_event', Events.keyPressed)
        
#        toolbar = NavigationToolbar2QT(canvas)
#        toolbar.update()

        self.show()

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

class fMenu:
    def file_open():
        global ani,fileName,data,VROT,RADI,historyList,xScale,yScale,key,numPrecisionY,numPrecisionX,app,par,NUR
        
        fileName = QtGui.QFileDialog.getOpenFileName()
        print (fileName)
#        fileName = open(fileName,'r')
        
        
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
            animation.FuncAnimation(f, animate, interval=500)
        else:
#            global app
            if len(VROT)==0:
                sys.exit(app.exec_())
        

    def close_application():
        choice = QtGui.QMessageBox.question('Exit!',
                                            "Are you sure?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Exiting Now")
            sys.exit()
        else:
            pass
        
        

    
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())   


"""
Global variables
"""
global app
LARGE_FONT= ("Verdana", 12)
SMALL_FONT= ("Verdana", 9)
style.use("ggplot")

f = Figure()
a = f.add_subplot(111)

historyList={}
xScale=[0,5]
yScale=[0,25]
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


parVals = {'RADI':RADI[:],'VROT':VROT[:]}

run()  