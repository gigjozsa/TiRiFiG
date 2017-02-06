# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:49:38 2017

@author: samuel
"""

from PyQt4 import QtGui
import os, sys
import numpy as np
from math import ceil 
import matplotlib.animation as animation
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

class PrettyWidget(QtGui.QWidget):
    
#    f = Figure()
#    a = f.add_subplot(111)
    key = "Yes"
    precisionPAR = 1
    precisionRADI = 1
    numPrecisionY = 0
    numPrecisionX = 0
    NUR = [0]
    data = []
    VROT = []
    RADI = [0]
    historyList={}
    xScale=[0,0]
    yScale=[0,0]
    fileName = None
    key = "Yes"
    par = 'VROT'
    unitMeas = 'km/s'
    mPress=[-5+min(RADI)];mRelease=['None'];mMotion=[-5+min(RADI)]
    parVals = {'RADI':RADI[:],'VROT':VROT[:]}
    
    
    
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()
        
        
    def initUI(self):
        self.setGeometry(600,300, 1000, 600)
        self.center()
        self.setWindowTitle('Revision on Plots, Tables and File Browser')     
        
        #Grid Layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
                    
        #Canvas and Toolbar
        self.figure = plt.figure(figsize=(15,5))    
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self)
#        self.canvas = FigureCanvas(self.f)
        
        self.canvas.mpl_connect('button_press_event', self.getClick)
        self.canvas.mpl_connect('button_release_event', self.getRelease)
        self.canvas.mpl_connect('motion_notify_event', self.getMotion)
        self.canvas.mpl_connect('key_press_event', self.keyPressed)
        
#        self.toolbar = NavigationToolbar(self.canvas, self)
#        toolbar.update()
        grid.addWidget(self.canvas, 2,0,1,2)
        grid.addWidget(self.toolbar, 1,0,1,2)

        #Empty 5x5 Table
        self.table = QtGui.QTableWidget(self)
        self.table.setRowCount(1)
        self.table.setColumnCount(9)
        grid.addWidget(self.table, 3,0,1,2)
        
        #Import def Button
        btn1 = QtGui.QPushButton('Import Def', self)
        btn1.resize(btn1.sizeHint()) 
        btn1.clicked.connect(self.openDef)
        grid.addWidget(btn1, 0,0)
        
        #Plot Button
        btn2 = QtGui.QPushButton('Plot', self)
        btn2.resize(btn2.sizeHint())    
        btn2.clicked.connect(self.plot)
        grid.addWidget(btn2, 0,1)
    
        self.show()
        
    
    
    def getPath(self):
        
        filePath = QtGui.QFileDialog.getOpenFileName(self)
#        fileHandle = open(filePath, 'r')
        return filePath
    
    
    def getData(self,filePath):
        
        with open(filePath) as f:
            data = f.readlines()
        f.close()
        return data
        
    def numPrecision(self,sKey,data):
        decPoints = []
    
        for i in range(len(data)):
            val = data[i].split(".")
            #make sure val has two elements
            if len(val)==2:
                decPoints.append(len(val[1]))
        
        if not(sKey == "RADI"):
            if len(decPoints)==0:
                PrettyWidget.precisionPAR = 0
            else:
                PrettyWidget.precisionPAR = max(decPoints)
        else:
            if len(decPoints)==0:
                PrettyWidget.precisionRADI = 0
            else:
                PrettyWidget.precisionRADI = max(decPoints) 
    
    def openDef(self):
        
        fileName = self.getPath()
        if (not(fileName==None) and not(len(fileName)==0)):
            self.data = self.getData(fileName)
            self.VROT = self.getParameter("VROT",self.data)
#            print (self.VROT)
            self.RADI = self.getParameter("RADI",self.data)
#            print (self.RADI)
            self.parVals = {'RADI':self.RADI[:],'VROT':self.VROT[:]}
            self.numPrecisionY = self.precisionPAR
            self.numPrecisionX = self.precisionRADI
            #ensure there are the same points for VROT as there are for RADI as specified in NUR parameter
            self.NUR = self.getParameter("NUR",self.data)
            diff = self.NUR[0]-len(self.VROT)
            lastIndexItem = len(self.VROT)-1
            if diff == self.NUR[0]:
                for i in range(int(diff)):
                    self.VROT.append(0.0)
            elif diff > 0 and diff < self.NUR[0]:
                for i in range(int(diff)):
                    self.VROT.append(self.VROT[lastIndexItem])
            
            self.historyList.clear()
            self.historyList[self.par] = [self.VROT[:]]
            if (max(self.RADI)-min(self.RADI))<=100:
                self.xScale = [int(ceil(-2*max(self.RADI))),int(ceil(2*max(self.RADI)))]                           
            else:
                self.xScale = [int(ceil(min(self.RADI)-0.1*(max(self.RADI)-min(self.RADI)))),int(ceil(max(self.RADI)+0.1*(max(self.RADI)-min(self.RADI))))]                            
                #print ('@if: ',len(VROTvals))
            if (max(self.VROT)-min(self.VROT))<=100:
                self.yScale = [int(ceil(-2*max(self.VROT))),int(ceil(2*max(self.VROT)))]
            else:
                self.yScale = [int(ceil(min(self.VROT)-0.1*(max(self.VROT)-min(self.VROT)))),int(ceil(max(self.VROT)+0.1*(max(self.VROT)-min(self.VROT))))]
                #print ('@if: ',len(VROTvals))
        else:
#            global app
            if len(self.VROT)==0:
                sys.exit(0)
    
    
        
    def getParameter(self,sKey,data):
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
                self.numPrecision(sKey,parVal)
            if not(sKey == "RADI"):
                precision = self.precisionPAR
            else:
                precision = self.precisionRADI
                
            for i in range(len(parVal)):
                parVal[i]=round(float(parVal[i]),precision)
            return parVal   
        else:
            zeroValues = []
            for i in range(int(self.NUR[0])):
                zeroValues.append(0.0)
            self.precisionPAR = 1
            return zeroValues
#            print("Search key not found")
        

        
#        line = fileHandle.readline()[:-1].split(',')
#        for n, val in enumerate(line):
#            newitem = QtGui.QTableWidgetItem(val)
#            self.table.setItem(0, n, newitem)
#        self.table.resizeColumnsToContents()
#        self.table.resizeRowsToContents()    
    
    
    def plot(self):
#        self.a.clear()
#        for ax in self.f.get_axes():
#            ax.set_xlabel("RADI (arcsec)")
#            ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
#    
#        self.a.plot(self.parVals['RADI'], self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
#        self.a.set_xlim(self.xScale[0],self.xScale[1])            
#        self.a.set_ylim(self.yScale[0],self.yScale[1])
        
        

        plt.cla()
        ax = self.figure.add_subplot(111)
        if self.key == "Yes":
            ax.plot(self.parVals['RADI'], self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
        else:
            ax.plot(self.parVals['RADI'], self.parVals[self.par],'--bo')
        ax.set_title('Plot')
        self.canvas.draw()
        
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def getClick(self,event):
        if event.xdata == None:
            pass
        else:
            self.mPress[0]=round(float(event.xdata),self.numPrecisionY)
            self.mRelease[0]="None"
            
    def getRelease(self,event):
        if not(event.ydata == None):
            self.mRelease[0]=round(float(event.ydata),self.numPrecisionY)
            if not(self.historyList[self.par][len(self.historyList[self.par])-1]==self.parVals[self.par][:]):
                self.historyList[self.par].append(self.parVals[self.par][:])
                self.mPress[0]=-5+min(self.RADI)
                self.mRelease[0]="None"
    
    def getMotion(self,event):
        if event.ydata == None:
            pass
        else:
            self.mMotion[0]=round(float(event.ydata),self.numPrecisionY)
    
    def keyPressed(self,event):
        if event.key == "ctrl+z" or event.key == "ctrl+Z":
            if len(self.historyList[self.par])>1:
                self.historyList[self.par].pop()
            #print('historyList after undo: ',historyList)
            tempHistoryList = self.historyList[self.par][len(self.historyList[self.par])-1]
            for i in range(len(self.parVals[self.par])):
                self.parVals[self.par][i]=round(tempHistoryList[i],self.numPrecisionY) 
            self.key = "Yes"
            
    def animate(self,i):
    
        if self.key=="Yes":
    #        a.clear()
    #        for ax in f.get_axes():
    #            ax.set_xlabel("RADI (arcsec)")
    #            ax.set_ylabel(par + "( "+unitMeas+ " )")
    #        print(historyList[par][len(historyList[par])-1])
    #        a.plot(parVals['RADI'], historyList[par][len(historyList[par])-1],'--bo')
    #        a.set_xlim(xScale[0],xScale[1])            
    #        a.set_ylim(yScale[0],yScale[1]) 
            self.plot()
            self.key = "No"
        
        for j in range(len(self.parVals['RADI'])):
            if (self.mPress[0] < (self.parVals['RADI'][j])+3) and (self.mPress[0] > (self.parVals['RADI'][j])-3) and (self.mRelease[0]=="None"):
                self.parVals[self.par][j] = self.mMotion[0]
                #print("historyList in motion: ",historyList)
#                a.clear()
    #            for ax in f.get_axes():
    #                ax.set_xlabel("RADI (arcsec)")
    #                ax.set_ylabel(par + "( "+unitMeas+ " )")
    #            a.plot(parVals['RADI'], parVals[par],'--bo')
                self.plot()
    #            print("mMotion:",mMotion," yScale:",yScale)
                if (self.yScale[1] - self.mMotion[0])<=50:
                    self.yScale[1] += 50
                elif (self.mMotion[0] - self.yScale[0])<= 50:
                    self.yScale[0] -= 50
#                a.set_xlim(xScale[0],xScale[1])            
#                a.set_ylim(yScale[0],yScale[1])
    
    
        
def main():
    app = QtGui.QApplication(sys.argv)
    w = PrettyWidget()
    ani=animation.FuncAnimation(PrettyWidget.figure, PrettyWidget.animate, interval=500)
    app.exec_()




if __name__ == '__main__':
    main()