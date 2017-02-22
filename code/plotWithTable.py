    # -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:49:38 2017

@author: samuel

This script here is the GUI (PyQt) implementation of TiRiFiC. As of now the code has been
written in Python 3. Future considerations would be made to have it run on Python 2.7 as
well.
"""


from PyQt4 import QtGui, QtCore
import os, sys
import numpy as np
from math import ceil 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

class PrettyWidget(QtGui.QWidget):
    """
    This class ...
    
    
    Parameters
    ----------
    arg1: <dataType>
        description of arg1
        
    Variables
    ---------
    
        
    
    """
    
    key = "Yes"
    precisionPAR = 0
    precisionRADI = 0
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
    par = 'VROT'
    unitMeas = 'km/s'
    mPress=[-5+min(RADI)];mRelease=['None'];mMotion=[-5+min(RADI)]
    parVals = {'RADI':RADI[:],'VROT':VROT[:]}
        
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()
        
    def initUI(self):
        
        self.setMinimumSize(1280, 720)
#        self.setGeometry(600, 300, 1000, 600)
#        self.setFixedSize(1450,250)
        self.center()
        self.setWindowTitle('Revision on Plots, Tables and File Browser')     
        
        #Grid Layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
                    
        #Canvas and Toolbar
        self.figure = plt.figure() 
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
#        self.canvas = FigureCanvas(self.f)
        self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.canvas.setFocus()
        
        self.canvas.mpl_connect('button_press_event', self.getClick)
        self.canvas.mpl_connect('button_release_event', self.getRelease)
        self.canvas.mpl_connect('motion_notify_event', self.getMotion)
        self.canvas.mpl_connect('key_press_event', self.keyPressed)
        
#        self.toolbar = NavigationToolbar(self.canvas, self)
#        toolbar.update()
        grid.addWidget(self.toolbar, 1,0,1,2)
        grid.addWidget(self.canvas, 2,0,1,2)
        

        #Empty 5x5 Table
#        self.table = QtGui.QTableWidget(self)
#        self.table.setRowCount(1)
#        self.table.setColumnCount(9)
#        grid.addWidget(self.table, 3,0,1,2)
        
        #Import def Button
        btn1 = QtGui.QPushButton('Import Def', self)
        btn1.resize(btn1.sizeHint()) 
        btn1.clicked.connect(self.openDef)
        grid.addWidget(btn1, 0,0)
        
        #Plot Button
        btn2 = QtGui.QPushButton('Plot', self)
        btn2.resize(btn2.sizeHint())    
        btn2.clicked.connect(self.firstPlot) 
        grid.addWidget(btn2, 0,1)
    
    
    def getData(self):
        """
        This function opens a file to read data
        
        The 
        """
    
        filePath = QtGui.QFileDialog.getOpenFileName(self,"Open .def File", "/home",".def Files (*.def)")
        
        if (not(filePath==None)) and (not len(filePath)==0):
            with open(filePath) as f:
                data = f.readlines()
            f.close()
        else:
            if (len(self.data)>0) or (not(self.data==None)):
                pass
            else:
                data = None
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
                self.precisionPAR = 0
            else:
                self.precisionPAR = max(decPoints)
        else:
            if len(decPoints)==0:
                self.precisionRADI = 0
            else:
                self.precisionRADI = max(decPoints)

        
    def openDef(self):

        self.data = self.getData()
        
        
        if not(self.data==None):
            self.VROT = self.getParameter("VROT",self.data)
            self.RADI = self.getParameter("RADI",self.data)
                
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
            
            self.parVals = {'RADI':self.RADI[:],'VROT':self.VROT[:]}
            
            self.historyList.clear()
            self.historyList[self.par] = [self.VROT[:]]
            

            if (max(self.RADI)-min(self.RADI))<=100:
                self.xScale = [int(ceil(-2*max(self.RADI))),int(ceil(2*max(self.RADI)))]                           
            else:
                self.xScale = [int(ceil(min(self.RADI)-0.1*(max(self.RADI)-min(self.RADI)))),int(ceil(max(self.RADI)+0.1*(max(self.RADI)-min(self.RADI))))]                            

            if (max(self.VROT)-min(self.VROT))<=100:
                self.yScale = [int(ceil(-2*max(self.VROT))),int(ceil(2*max(self.VROT)))]
            else:
                self.yScale = [int(ceil(min(self.VROT)-0.1*(max(self.VROT)-min(self.VROT)))),int(ceil(max(self.VROT)+0.1*(max(self.VROT)-min(self.VROT))))]
            

        
    def getParameter(self,sKey,data):
        
#        global numPrecision, precisionPAR, precisionRADI, NUR
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
            
            if not((sKey == "RADI") or (sKey == "NUR")):
                precision = self.precisionPAR
            elif not((sKey == "VROT") or (sKey == "NUR")):
                precision = self.precisionRADI
            else:
                precision = 0
                
            for i in range(len(parVal)):
                parVal[i]=round(float(parVal[i]),precision)
            return parVal   
        else:
            zeroValues = []
            for i in range(int(self.NUR[0])):
                zeroValues.append(0.0)
            self.precisionPAR = 1
            return zeroValues
        
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def getClick(self,event):
        
#        print("click x-y values before if statement")
#        print("xdata: ",event.xdata,", ydata: ",event.ydata)
#        print("x: ",event.x,", y: ",event.y)
#        print("button: ",event.button)
#        print("click: ",event)
            
        
        if (event.button == 1) and not(event.xdata == None):
            self.mPress[0]=round(float(event.xdata),self.numPrecisionY)
#            print("mPress after clicking: ",self.mPress[0])
            self.mRelease[0]=None
#            print("\n")
#            print ("radi: ",event.xdata)
#            print ("vrot: ",event.ydata)
            
            
    def getRelease(self,event):
        
#        print("release x-y values before if statement")
#        print("xdata: ",event.xdata,", ydata: ",event.ydata)
#        print("x: ",event.x,", y: ",event.y)
#        print("button: ",event.button)
#        print("release: ",event)
#        print("release x-y values before if statement")
#        print("x: ",event.xdata,", y: ",event.ydata)
        if not(event.ydata == None):
#            print("release: ",event.ydata)
            self.mRelease[0]=round(float(event.ydata),self.numPrecisionY)
        if not(self.historyList[self.par][len(self.historyList[self.par])-1]==self.parVals[self.par][:]):
            self.historyList[self.par].append(self.parVals[self.par][:])
        self.mPress[0]=None
#                self.mRelease[0]=None


    def getMotion(self,event):
        
        if (event.button == 1) and not(event.ydata == None):
            self.mMotion[0]=round(float(event.ydata),self.numPrecisionY)
            self.plotFunc()
    
    def keyPressed(self,event):
        
        if event.key == "ctrl+z" or event.key == "ctrl+Z":
            print ("undo triggered")
            if len(self.historyList[self.par])>1:
                self.historyList[self.par].pop()
            tempHistoryList = self.historyList[self.par][len(self.historyList[self.par])-1]
            for i in range(len(self.parVals[self.par])):
                self.parVals[self.par][i]=round(tempHistoryList[i],self.numPrecisionY) 
            self.key = "Yes"
            self.plotFunc()
    
    def firstPlot(self):
               
        self.key = "Yes"
#            plt.cla()
        for axes in self.figure.get_axes():
            axes.set_xlabel("RADI (arcsec)")
            axes.set_ylabel(self.par + "( "+self.unitMeas+ " )")
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_xlim(self.xScale[0],self.xScale[1])            
        ax.set_ylim(self.yScale[0],self.yScale[1])
        ax.plot(self.parVals['RADI'], self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
        ax.set_title('Plot')
        ax.set_xticks(self.parVals['RADI'])
        self.canvas.draw()
        self.key = "No"
        
        
        
        
        
    def plotFunc(self):
  
        
        if self.key=="Yes":
#            plt.cla()
            for axes in self.figure.get_axes():
                axes.set_xlabel("RADI (arcsec)")
                axes.set_ylabel(self.par + "( "+self.unitMeas+ " )")
            ax = self.figure.add_subplot(111)
            ax.clear()
            ax.plot(self.parVals['RADI'], self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
#            print ("parVal: ",self.parVals['RADI'])
            ax.set_title('Plot')
            ax.set_xticks(self.parVals['RADI'])
            self.canvas.draw()
            self.key = "No"
            
        
        for j in range(len(self.parVals['RADI'])):
#            print("mPress[0]: ",self.mPress[0])
#            print("parVals['RADI'][j]): ",self.parVals['RADI'][j])
            if (self.mPress[0] < (self.parVals['RADI'][j])+3) and (self.mPress[0] > (self.parVals['RADI'][j])-3) and (self.mRelease[0]==None):
                self.parVals[self.par][j] = self.mMotion[0]
#                print ("parVal: ",self.parVals['RADI'])
#                plt.cla()
                for axes in self.figure.get_axes():
                    axes.set_xlabel("RADI (arcsec)")
                    axes.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                ax = self.figure.add_subplot(111)
                ax.clear()
                ax.set_xlim(self.xScale[0],self.xScale[1])            
                ax.set_ylim(self.yScale[0],self.yScale[1])
                print (self.xScale, self.yScale)
                ax.plot(self.parVals['RADI'], self.parVals[self.par],'--bo')
                ax.set_title('Plot')
                ax.set_xticks(self.parVals['RADI'])
                self.canvas.draw()
                self.key = "No"
                if (self.yScale[1] - self.mMotion[0])<=50:
                    self.yScale[1] += 50
                elif (self.mMotion[0] - self.yScale[0])<= 50:
                   self.yScale[0] -= 50
                
                ax.set_xlim(self.xScale[0],self.xScale[1])            
                ax.set_ylim(self.yScale[0],self.yScale[1])

    
        
def main():
    app = QtGui.QApplication(sys.argv)
#    app.geometry("1280x720")
    GUI = PrettyWidget()
    GUI.show()
    app.exec_()



if __name__ == '__main__':
    main()
