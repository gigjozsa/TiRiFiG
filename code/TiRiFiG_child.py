    # -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:49:38 2017

@author: samuel

This script here is the GUI (PyQt) implementation of TiRiFiC. As of now the code has been
written in Python 3. Future considerations would be made to have it run on Python 2.7 as
well.

functions:
    main 

classes:
    PrettyWidget:
        Class variables:
            key
            precisionPAR
            precisionRADI
            numPrecisionY
            numPrecision
            NUR
            data
            VROT
            RADI
            historyList
            xScale
            yScale
            fileName
            par
            unitMeas
            mPress
            parVals
            
        Instance variables
        
        Methods:
            __init__
            iniUI
            close_application
            getData
            numPrecision
            openDef
            getParameter
            center
            getClick
            getRelease
            getMotion
            keyPressed
            firstPlot
            plotFunc
            saveFile
            saveAll
"""


from PyQt4 import QtGui, QtCore
import os
import sys
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
        self.setWindowTitle('TiRiFiG')     
        
        #Grid Layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        
       
        self.exitAction = QtGui.QAction("&Exit", self)
#        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip('Leave the app')
        self.exitAction.triggered.connect(self.close_application)

        self.openFile = QtGui.QAction("&Open File", self)
#        self.openFile.setShortcut("Ctrl+O")
        self.openFile.setStatusTip('Load .def file to be plotted')
        self.openFile.triggered.connect(self.openDef)
        
        self.saveChanges = QtGui.QAction("&Save", self)
#        openEditor.setShortcut("Ctrl+S")
        self.saveChanges.setStatusTip('Save changes to .def file')
        self.saveChanges.triggered.connect(self.saveAll)

#        self.QtGui.statusBar(self)

        self.mainMenu = QtGui.QMenuBar(self)
        
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.openFile)
        self.fileMenu.addAction(self.exitAction)
        self.fileMenu.addAction(self.saveChanges)       
        
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
    
    def close_application(self):
        """Exit application
        
        Keyword arguments:
        self -- this is the main window being displayed
                i.e. the current instance of the PrettyWidget class
        
        User action will be confirmed by popping up a yes/no prompt
        """
        #pop up message 
        choice = QtGui.QMessageBox.question('Exit!',
                                            "Are you sure?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass
    
    def getData(self):
        """Loads data from specified .def file in open dialog box
        
        Keyword arguments:
        self -- this is the main window being displayed
                i.e. the current instance of the PrettyWidget class
        
        Returns:
        data:list
        The text found in each line of the opened file
        
        data will be a none type variable if the fileName is invalid or no file is chosen
        """
        
        #stores file path of .def to fileName variable after user selects file in open dialog box
        self.fileName = QtGui.QFileDialog.getOpenFileName(self,"Open .def File", "/home",".def Files (*.def)")
        
        #assign texts of read lines to data variable if fileName is exists, else assign None
        if (not(self.fileName==None)) and (not len(self.fileName)==0):
            with open(self.fileName) as f:
                data = f.readlines()
            f.close()
        else:
            if (len(self.data)==0) or (self.data==None):
                data = None
        return data
        
    def numPrecision(self,sKey,data):
        """Determines and sets floating point precision 
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        sKey (str) --   parameter search key
        data (list) --  list of values of type string e.g. x = ["20.3","55.0003","15.25","12.71717"]
        
        Returns:
        None
        
        Determines the highest floating point precision of data points
        and re-assigns parameter precision class variables (precisionPAR & precisionRADI) 
        as such
        """
        
        decPoints = []
    
        for i in range(len(data)):
            val = data[i].split(".")
            
            #check val has decimal & fractional part and append length of numbers of fractional part
            if len(val)==2:
                decPoints.append(len(val[1]))
        
        #assign greatest precision in decPoints to class variables handling precision
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
        """Opens data, gets parameters values, sets precision and sets scale
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        
        Returns:
        None
        
        Makes function calls to getData and getParameter functions, assigns values to dictionaries
        parVals and historyList and defines the x-scale and y-scale for plotting
        on viewgraph
        """  

        self.data = self.getData()
        
        
        if (not(self.data==None) or len(self.data)>0):
            self.VROT = self.getParameter("VROT",self.data)
            self.RADI = self.getParameter("RADI",self.data)
               
            """this line may not be necessary"""
#            self.numPrecisionY = self.precisionPAR
#            self.numPrecisionX = self.precisionRADI
            
#           ensure there are the same points for VROT as there are for RADI as specified in NUR parameter
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
            
            #defining the x and y scale for plotting
            if (max(self.RADI)-min(self.RADI))<=100:
                self.xScale = [int(ceil(-2*max(self.RADI))),int(ceil(2*max(self.RADI)))]                           
            else:
                self.xScale = [int(ceil(min(self.RADI)-0.1*(max(self.RADI)-min(self.RADI)))),int(ceil(max(self.RADI)+0.1*(max(self.RADI)-min(self.RADI))))]                            

            if (max(self.VROT)-min(self.VROT))<=100:
                self.yScale = [int(ceil(-2*max(self.VROT))),int(ceil(2*max(self.VROT)))]
            else:
                self.yScale = [int(ceil(min(self.VROT)-0.1*(max(self.VROT)-min(self.VROT)))),int(ceil(max(self.VROT)+0.1*(max(self.VROT)-min(self.VROT))))]
            

        
    def getParameter(self,sKey,data):
        """Fetches data points of specified parameter in search key
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        sKey (str) --   parameter search key
        data (list) --  list containing texts of each line loaded from .def file
        
        Returns:
        parVal:list
        The values appearing after the '=' symbol of the parameter specified in sKey.
        If search key isnt found, zero values are returned
        
        The data points for the specific parameter value are located and converted 
        from string to float data types for plotting and other data manipulation
        """
        #search through fetched data for values of "PAR =" or "PAR = " or "PAR=" or "PAR= "
        status = False
        for i in data:
            lineVals = i.split("=")
            if (len(lineVals)>1):
                lineVals[0] = ''.join(lineVals[0].split())
                if (sKey == lineVals[0]):
                    parVal = lineVals[1].split()
                    status = True
                    break
                
        #if found, obtain floating point precision and ensure all numbers have the same accuracy    
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
        """Centers the window
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        
        Returns:
        None
        
        With information from the user's desktop, the screen resolution is  gotten
        and the center point is figured out for which the window is placed.
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def getClick(self,event):
        """Left mouse button is pressed
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        event --        event type
        
        Returns:
        None
        
        The xData is captured when the left mouse button is clicked on the canvas
        """     
        #on left click in figure canvas, captures mouse press and assign None to 
        #mouse release
        if (event.button == 1) and not(event.xdata == None):
            self.mPress[0]=round(float(event.xdata),self.precisionPAR)
            self.mRelease[0]=None
            
            
    def getRelease(self,event):   
        """Left mouse button is released
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        event --        event type
        
        Returns:
        None
        
        The xData is captured when the left mouse button is released on the canvas.
        The new data point is added to the history and mouse pressed is assigned None
        """
        #re-look at this logic --seems to be a flaw somewhere
        if not(event.ydata == None):
            self.mRelease[0]=round(float(event.ydata),self.numPrecisionY)
            
        #append the new point to the history if the last item in history differs
        #from the new point
        if not(self.historyList[self.par][len(self.historyList[self.par])-1]==self.parVals[self.par][:]):
            self.historyList[self.par].append(self.parVals[self.par][:])
            
        self.mPress[0]=None
#                self.mRelease[0]=None


    def getMotion(self,event):
        """Mouse is in motion
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        event --        event type
        
        Returns:
        None
        
        The xData is captured when the left mouse button is released on the canvas.
        The new data point is added to the history and mouse pressed is assigned None
        """
        #whilst the left mouse button is being clicked and mouse pointer hasnt (why not use mPress=None instead of event.button = 1)
        #moved out of the figure canvas, capture the VROT (y-value) during mouse
        #movement and call re-draw graph
        if (event.button == 1) and not(event.ydata == None):
            self.mMotion[0]=round(float(event.ydata),self.numPrecisionY)
            self.plotFunc()
    
    def keyPressed(self,event):
        """Key is pressed
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        event --        event type
        
        Returns:
        None
        
        Deletes the last item in the history list when "Ctrl+z" is pressed and
        re-draws graph
        """
        if event.key == "ctrl+z" or event.key == "ctrl+Z":
            #history list musn't be empty
            if len(self.historyList[self.par])>1:
                self.historyList[self.par].pop()
                tempHistoryList = self.historyList[self.par][len(self.historyList[self.par])-1]
                #re-assign parVal to hold last list values in history list dictionary
                #and re-draw graph
                for i in range(len(self.parVals[self.par])):
                    self.parVals[self.par][i]=round(tempHistoryList[i],self.numPrecisionY) 
                self.key = "Yes"
                self.plotFunc()
            else:
                #pop up a messageBox saying history list is exhausted
                print("history is empty")
            
    
    def firstPlot(self):
        """Plots data from file
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        
        Returns:
        None
        
        Produces view graph from historyList
        """
        self.key = "Yes"
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
        """Plots data from file
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        
        Returns:
        None
        
        Produces view graph from historyList or parVals
        """
        #why dont you just call firstPlot function instead of typing the same thing again
        if self.key=="Yes":
            for axes in self.figure.get_axes():
                axes.set_xlabel("RADI (arcsec)")
                axes.set_ylabel(self.par + "( "+self.unitMeas+ " )")
            ax = self.figure.add_subplot(111)
            ax.clear()
            ax.plot(self.parVals['RADI'], self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
            ax.set_title('Plot')
#            ax.set_xticks(self.parVals['RADI'])
            self.canvas.draw()
            self.key = "No"
            
        #this re-plots the graph as long as the mouse is in motion and the right
        #data point is clicked
        for j in range(len(self.parVals['RADI'])):
            if (self.mPress[0] < (self.parVals['RADI'][j])+3) and (self.mPress[0] > (self.parVals['RADI'][j])-3) and (self.mRelease[0]==None):
                self.parVals[self.par][j] = self.mMotion[0]
                for axes in self.figure.get_axes():
                    axes.set_xlabel("RADI (arcsec)")
                    axes.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                ax = self.figure.add_subplot(111)
                ax.clear()
                ax.set_xlim(self.xScale[0],self.xScale[1])            
                ax.set_ylim(self.yScale[0],self.yScale[1])
                ax.plot(self.parVals['RADI'], self.parVals[self.par],'--bo')
                ax.set_title('Plot')
#                ax.set_xticks(self.parVals['RADI'])
                self.canvas.draw()
                self.key = "No"
                if (self.yScale[1] - self.mMotion[0])<=50:
                    self.yScale[1] += 50
                elif (self.mMotion[0] - self.yScale[0])<= 50:
                   self.yScale[0] -= 50
                
                ax.set_xlim(self.xScale[0],self.xScale[1])            
                ax.set_ylim(self.yScale[0],self.yScale[1])

    
    def saveFile(self,newVals,sKey):  
        """Save changes made to data points to .def file per specified parameter
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the PrettyWidget class
        newVals (list) --  list containing new values
        sKey (str) --   parameter search key
        
        Returns:
        None
        
        The .def file would be re-opened and updated per the new values that
        are contained in the parVal* variable 
        """
        
        if sKey == 'RADI':
            r = self.numPrecisionX
        else:
            r = self.numPrecisionY
            
        #get the new values and format it as [0 20 30 40 50...]
        txt =""
        for i in range(len(newVals)):
            txt = txt+" " +'{0:.{1}f}'.format(newVals[i], r)

            #txt = txt+" " + str(newVals[i])

        tmpFile=[]
        with open(self.fileName,'a') as f:
            status = False
            for i in self.data:
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
                tmpFile.append("# "+self.par+" parameter in "+self.unitMeas+"\n")
                txt = "    "+sKey+"="+txt+"\n"
                tmpFile.append(txt)
                
            f.seek(0)
            f.truncate()
            for i in tmpFile:
                f.write(i)
            
            self.data = tmpFile[:]
            f.close()
            
    def saveAll(self):
        """Save changes made to data point to .def file for all parameters
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of 
        the PrettyWidget class
        
        Returns:
        None
        
        The saveFile function is called and updated with the current values being 
        held by parameters in the view graph.
        """
        for i in self.parVals:
            self.saveFile(self.parVals[i],i)
        
    
        
def main():
    app = QtGui.QApplication(sys.argv)
#    app.geometry("1280x720")
    GUI = PrettyWidget()
    GUI.show()
    app.exec_()



if __name__ == '__main__':
    main()
