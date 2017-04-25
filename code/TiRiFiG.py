# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:43:03 2017

@author: Samuel
"""
#libraries
from PyQt4 import QtGui, QtCore
import os
import sys
import numpy as np
from math import ceil 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

#classes

class GraphWidget(QtGui.QWidget):
    
    key = "Yes"
    scaleChange = "No"
    choice = "Beyond Viewgraph"
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
    yVal = 0
    parVals = {'RADI':RADI[:],'VROT':VROT[:]}
    
    
    
    def __init__(self):
        super(GraphWidget, self).__init__()
        #Grid Layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        self.setMinimumSize(1280,720)
        self.center()
        
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
        
        grid.addWidget(self.toolbar, 1,0,1,2)
        grid.addWidget(self.canvas, 2,0,1,2)

        #Import def Button
        btn1 = QtGui.QPushButton('Import Def', self)
        btn1.minimumSize()
        btn1.clicked.connect(self.openDef)
        grid.addWidget(btn1, 0,0)
        
#        Plot Button
        btn2 = QtGui.QPushButton('Plot', self)
        btn2.resize(btn2.sizeHint())    
        btn2.clicked.connect(self.firstPlot) 
        grid.addWidget(btn2, 0,1)
            
    def center(self):
        """Centers the window
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        With information from the user's desktop, the screen resolution is  gotten
        and the center point is figured out for which the window is placed.
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def close_application(self):
        """Exit application
        
        Keyword arguments:
        self -- this is the main window being displayed
                i.e. the current instance of the mainWindow class
        
        User action will be confirmed by popping up a yes/no prompt
        """
        #message box for action confirmation
        choice = QtGui.QMessageBox.question(self,'Exit Application',
                                            "Are you sure?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit(0)
        else:
            print ("Yes wasnt detected")
            pass
    
    def getData(self):
        """Loads data from specified .def file in open dialog box
        
        Keyword arguments:
        self -- this is the main window being displayed
                i.e. the current instance of the mainWindow class
        
        Returns:
        data:list
        The text found in each line of the opened file
        
        data will be a none type variable if the fileName is invalid or no file is chosen
        """
        
        #stores file path of .def to fileName variable after user selects file in open dialog box
        self.fileName = QtGui.QFileDialog.getOpenFileName(self,"Open .def File", os.getcwd(),".def Files (*.def)")
        
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
        self --         main window being displayed i.e. the current instance of the mainWindow class
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
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Makes function calls to getData and getParameter functions, assigns values to dictionaries
        parVals and historyList and defines the x-scale and y-scale for plotting
        on viewgraph
        """  

        self.data = self.getData()
        
        if self.data == None:
            pass
        elif (not(self.data==None) or len(self.data)>0):
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
        self --         main window being displayed i.e. the current instance of the mainWindow class
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
            
        
    def getClick(self,event):
        """Left mouse button is pressed
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        event --        event type
        
        Returns:
        None
        
        The xData is captured when the left mouse button is clicked on the canvas
        """     
        #on left click in figure canvas, captures mouse press and assign None to 
        #mouse release
        if (event.button == 1) and not(event.xdata == None):
            self.mPress[0]=round(float(event.xdata),self.precisionPAR)
            self.yVal = round(float(event.ydata),self.numPrecisionY)
            self.mRelease[0]=None
        
        """if self.plot == "bingo":
            print("It worked")
            print (self.xScale)
            print(self.yScale)
            self.plotFunc()
            self.plot = "No"
            """
            
    def getRelease(self,event):   
        """Left mouse button is released
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
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
        self --         main window being displayed i.e. the current instance of the mainWindow class
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
        self --         main window being displayed i.e. the current instance of the mainWindow class
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

                if (max(self.parVals[self.par])-min(self.parVals[self.par]))<=100:
                    self.yScale = [int(ceil(-2*max(self.parVals[self.par]))),int(ceil(2*max(self.parVals[self.par])))]
                else:
                    self.yScale = [int(ceil(min(self.parVals[self.par])-0.1*(max(self.parVals[self.par])-min(self.parVals[self.par])))),int(ceil(max(self.parVals[self.par])+0.1*(max(self.parVals[self.par])-min(self.parVals[self.par]))))]
                
                self.key = "Yes"
                self.plotFunc()
            else:
                #pop up a messageBox saying history list is exhausted
#                print("history is empty")
                self.showInformation()
       
         
    def showInformation(self):
        """Show the information message
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Displays a messagebox that informs user there's no previous action to be undone
        """
        QtGui.QMessageBox.information(self, "Information", "History list is exhausted")
        
        
    def firstPlot(self):
        """Plots data from file
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Produces view graph from historyList
        """
        

        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_xlim(self.xScale[0],self.xScale[1])            
        ax.set_ylim(self.yScale[0],self.yScale[1])
        for axes in self.figure.get_axes():
            axes.set_xlabel("RADI (arcsec)")
            axes.set_ylabel(self.par + "( "+self.unitMeas+ " )")
        ax.plot(self.parVals['RADI'], self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
        ax.set_title('Plot')
        ax.set_xticks(self.parVals['RADI'])
#        ax.set_yticks(np.arange(min(self.parVals[self.par]),max(self.parVals[self.par])+1,500))
        self.canvas.draw()
        self.key = "No"
        
        
        
    def plotFunc(self):
        """Plots data from file
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Produces view graph from historyList or parVals
        """
        if self.scaleChange == "Yes":
            ax = self.figure.add_subplot(111)
            ax.clear()
            ax.set_xlim(self.xScale[0],self.xScale[1])
            ax.set_ylim(self.yScale[0],self.yScale[1])
            for axes in self.figure.get_axes():
                axes.set_xlabel("RADI (arcsec)")
                axes.set_ylabel(self.par + "( "+self.unitMeas+ " )")
            ax.plot(self.parVals['RADI'], self.parVals[self.par],'--bo')
            ax.set_title('Plot')
            #ax.set_xticks(self.parVals['RADI'])
            self.canvas.draw() 
            self.scaleChange = "No"
        
        if self.key=="Yes":
            self.firstPlot()
            
        #this re-plots the graph as long as the mouse is in motion and the right
        #data point is clicked
        else:
            for j in range(len(self.parVals['RADI'])):
                if (self.mPress[0] < (self.parVals['RADI'][j])+3) and (self.mPress[0] > (self.parVals['RADI'][j])-3) and (self.mRelease[0]==None):
                    self.parVals[self.par][j] = self.mMotion[0]
                    ax = self.figure.add_subplot(111)
                    ax.clear()
                    ax.set_xlim(self.xScale[0],self.xScale[1])            
#                    print (self.choice)
                    if self.choice == "Beyond Viewgraph":
                        if (self.yScale[1] - self.mMotion[0])<=200:
                            self.yScale[1] += 100
                        elif (self.mMotion[0] - self.yScale[0])<= 200:
                            self.yScale[0] -= 100
                        
                    elif self.choice == "Free":
                        if self.mMotion[0]>self.yVal:
                            if ((self.yScale[1]-max(self.parVals[self.par]))<=300) and ((max(self.parVals[self.par])-self.mMotion[0])<=20):
                                self.yScale[1] += 200
                            elif abs(self.yScale[0] - min(self.parVals[self.par]))>=300:
                                self.yScale[0] += 200
                        elif self.mMotion[0]<self.yVal:
                            if ((min(self.parVals[self.par])-self.yScale[0])<=300) and ((min(self.parVals[self.par])-self.mMotion[0])<=20):
                                self.yScale[0] -= 200
                            elif abs(self.yScale[1] - max(self.parVals[self.par]))>=300:
                                self.yScale[1] -= 200
                    print ("after koraa: ",self.yScale)
                    ax.set_ylim(self.yScale[0],self.yScale[1])
                    for axes in self.figure.get_axes():
                        axes.set_xlabel("RADI (arcsec)")
                        axes.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                    ax.plot(self.parVals['RADI'], self.parVals[self.par],'--bo')
                    ax.set_title('Plot')
                  #  ax.set_xticks(self.parVals['RADI'])
#                    ax.set_yticks(np.arange(min(self.parVals[self.par]),max(self.parVals[self.par])+1,200))
                    self.canvas.draw()                

    
    def saveFile(self,newVals,sKey):  
        """Save changes made to data points to .def file per specified parameter
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
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
        #put this block of code in a try except block
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
        the mainWindow class
        
        Returns:
        None
        
        The saveFile function is called and updated with the current values being 
        held by parameters.
        """
        for i in self.parVals:
            self.saveFile(self.parVals[i],i)
    
    def saveMessage(self):
        """Displays the information about save action
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Displays a messagebox that informs user that changes have been successfully written to the .def file
        """
        QtGui.QMessageBox.information(self, "Information", "Changes successfully written to file")
        
    def saveAs(self,fileName,newVals,sKey):  
        """Creates a new .def file with current data points on viewgraph
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        fileName --     filePath where new file should be saved to
        newVals (list) --  list containing new values
        sKey (str) --   parameter search key
        
        Returns:
        None
        
        A new .def file would be created and placed in the specified file path
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
        
        
        if not(fileName==None):
            with open(fileName,'a') as f:
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
    
    def saveAsAll(self):
        """Creates a new .def file for all parameters in current .def file opened
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of 
        the mainWindow class
        
        Returns:
        None
        
        The saveAs function is called and updated with the current values being 
        held by parameters.
        """
        fileName = QtGui.QFileDialog.getSaveFileName(self,"Save .def file as ",os.getcwd(),
                                                    ".def Files (*.def)")
        
        for i in self.parVals:
            self.saveAs(fileName,self.parVals[i],i)
    
    def startTiriFiC(self):
        """Start TiRiFiC
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of 
        the mainWindow class
        
        Returns:
        None
        
        Calls the os.system and opens terminal to start TiRiFiC
        """
        os.system("gnome-terminal -e 'bash -c \"/home/samuel/software/TiRiFiC/tirific_2.3.4/bin/tirific deffile = "+self.fileName+"; exec bash\"'")
    
    def openEditor(self):
        text,ok = QtGui.QInputDialog.getText(self,'Text Editor Input Dialog', 
                                            'Enter text editor:')
        
        if ok:
            if len(text)>0:
                programName = str(text)
                os.system("gnome-terminal -e 'bash -c \""+programName+" "+self.fileName+"; exec bash\"'")
            else:
                os.system("gnome-terminal -e 'bash -c \"gedit "+self.fileName+"; exec bash\"'")
    

class SMWindow(QtGui.QWidget):
#    xScale = [0,0]
#    yScale = [0,0]
    
    def __init__(self):
        super(SMWindow, self).__init__()
        

        self.xMin = QtGui.QLineEdit()
        self.xMin.minimumSize()
        self.xMin.setPlaceholderText("RADI min")        
        self.xMax = QtGui.QLineEdit()
        self.xMax.minimumSize()
        self.xMax.setPlaceholderText("RADI max")
       
        self.yMin = QtGui.QLineEdit()
        self.yMin.minimumSize()
        self.yMin.setPlaceholderText(GraphWidget.par+" min") 
        self.yMax = QtGui.QLineEdit()
        self.yMax.minimumSize()
        self.yMax.setPlaceholderText(GraphWidget.par+" max")
    
    
        self.fbox = QtGui.QFormLayout(self)
       
        self.fbox.addRow(self.xMin)
        self.fbox.addRow(self.xMax)
        self.fbox.addRow(self.yMin)
        self.fbox.addRow(self.yMax)
    
        self.hbox = QtGui.QHBoxLayout()
    
        self.radioFree = QtGui.QRadioButton("Free")
       # self.radioFree.clicked.connect(self.getOptF)
        self.radioViewG = QtGui.QRadioButton("Beyond Viewgraph")
        #self.radioViewG.clicked.connect(self.getOptV)
        
        self.hbox.addWidget(self.radioFree)
        self.hbox.addWidget(self.radioViewG)
        self.hbox.addStretch()
        self.fbox.addRow(QtGui.QLabel("Scale Behaviour"),self.hbox)
       
        self.btnUpdate = QtGui.QPushButton('Update', self)
       # self.btnUpdate.clicked.connect(self.updateScale)
        self.btnUpdate.minimumSize()
        self.btnCancel = QtGui.QPushButton('Cancel', self)
        #self.btnCancel.clicked.connect(self.close)
        self.btnCancel.minimumSize()
        self.fbox.addRow(self.btnUpdate,self.btnCancel) 
    
        self.setLayout(self.fbox)
        self.setFocus()
        self.setWindowTitle("Scale Manager")
#        self.setMinimumSize(1280, 720)
        self.minimumSizeHint()
        

class ParamSpec(QtGui.QWidget):
    
    def __init__(self):
        super(ParamSpec, self).__init__()

        self.parameter = QtGui.QLineEdit()
        self.parameter.minimumSize()
        self.parameter.setPlaceholderText("Parameter")        
        self.unitMeasurement = QtGui.QLineEdit()
        self.unitMeasurement.minimumSize()
        self.unitMeasurement.setPlaceholderText("Unit Measurement")
      
    
    
        self.fbox = QtGui.QFormLayout(self)
       
        self.fbox.addRow(self.parameter)
        self.fbox.addRow(self.unitMeasurement)
        
    
        
       
        self.btnOK = QtGui.QPushButton('OK', self)
        
        self.btnOK.minimumSize()
        self.btnCancel = QtGui.QPushButton('Cancel', self)
        
        self.btnCancel.minimumSize()
        self.fbox.addRow(self.btnOK,self.btnCancel) 
    
        self.setLayout(self.fbox)
       
        self.setWindowTitle("Parameter Definition")
#        self.setMinimumSize(1280, 720)
        self.minimumSizeHint()
        self.setFocus()

class mainWindow(QtGui.QMainWindow):
    
   def __init__(self):
        super(mainWindow, self).__init__()
        self.initUI()
    
   def initUI(self):
        
        self.gw = GraphWidget()
        self.setCentralWidget(self.gw)
        self.sm = SMWindow()
        self.ps = ParamSpec()
        self.setMinimumSize(1280, 720)
#        self.setGeometry(600, 300, 1000, 600)
#        self.setFixedSize(1450,250)
        self.createActions()
        self.createMenus()
        self.setWindowTitle('TiRiFiG') 
        self.gw.center()
       
   def createActions(self):
        self.exitAction = QtGui.QAction("&Exit", self)
#        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip('Leave the app')
        self.exitAction.triggered.connect(self.gw.close_application)

        self.openFile = QtGui.QAction("&Open File", self)
#        self.openFile.setShortcut("Ctrl+O")
        self.openFile.setStatusTip('Load .def file to be plotted')
        self.openFile.triggered.connect(self.gw.openDef)
        
        self.saveChanges = QtGui.QAction("&Save", self)
#        openEditor.setShortcut("Ctrl+S")
        self.saveChanges.setStatusTip('Save changes to .def file')
        self.saveChanges.triggered.connect(self.gw.saveAll)
        
        self.saveAs = QtGui.QAction("&Save as...",self)
        self.saveAs.setStatusTip('Create another .def file with current paramater values')
        self.saveAs.triggered.connect(self.gw.saveAsAll)
        
        self.openTextEditor = QtGui.QAction("&Open Text Editor...",self)
        self.openTextEditor.setStatusTip('View the current open .def file in preferred text editor')
        self.openTextEditor.triggered.connect(self.gw.openEditor) # function yet to be written
        
        self.startTF = QtGui.QAction("&Start TiriFiC",self)
        self.startTF.setStatusTip('Starts TiRiFiC from terminal')
        self.startTF.triggered.connect(self.gw.startTiriFiC)
        
        self.scaleMan = QtGui.QAction("&Scale Manager",self)
        self.scaleMan.setStatusTip('Manages behaviour of scale and min and max values')
        self.scaleMan.triggered.connect(self.sm.show)
        
        self.paraDef = QtGui.QAction("&Parameter Definition",self)
        self.paraDef.setStatusTip('Determines which parameter is plotted on the y-axis')
        self.paraDef.triggered.connect(self.ps.show)
        
#        self.QtGui.statusBar(self)
        
        self.sm.radioFree.clicked.connect(self.getOptF)
        self.sm.radioViewG.clicked.connect(self.getOptV)
        self.sm.btnUpdate.clicked.connect(self.updateScale)
        self.sm.btnCancel.clicked.connect(self.sm.close)
        self.ps.btnOK.clicked.connect(self.paramDef)
        self.ps.btnCancel.clicked.connect(self.close)

   def createMenus(self):
        mainMenu = self.menuBar()
        
        self.fileMenu = mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.openFile)
        self.fileMenu.addAction(self.saveChanges)
        self.fileMenu.addAction(self.saveAs)
        self.fileMenu.addAction(self.exitAction)
        
#        editMenu = mainMenu.addMenu('&Edit')
       
        self.runMenu = mainMenu.addMenu('&Run')
        self.runMenu.addAction(self.openTextEditor)
        self.runMenu.addAction(self.startTF)
        
        self.prefMenu = mainMenu.addMenu('&Preferences')
        self.prefMenu.addAction(self.scaleMan)
        self.prefMenu.addAction(self.paraDef)

   def getOptF(self):
        self.gw.choice = "Free"
    
   def getOptV(self):
        self.gw.choice = "Beyond Viewgraph"
        
   def updateScale(self):

        if len(self.sm.yMin.text())>0:
            self.gw.yScale[0] = int(ceil(float(self.sm.yMin.text())))
            
        if len(self.sm.yMax.text())>0:
            self.gw.yScale[1] = int(ceil(float(self.sm.yMax.text())))
            
        if len(self.sm.xMin.text())>0:
            self.gw.xScale[0] = int(ceil(float(self.sm.xMin.text())))
            
        if len(self.sm.xMax.text())>0:
            self.gw.xScale[1] = int(ceil(float(self.sm.xMax.text())))
            
        self.gw.scaleChange = "Yes"       
        self.gw.plotFunc()      
        self.sm.close()        
        
   def paramDef(self):
       
       if len(self.ps.parameter.text())>0 and not(str(self.ps.parameter) == self.gw.par):
           self.gw.par = str(self.ps.parameter.text())
           self.gw.unitMeas = str(self.ps.unitMeasurement.text())
           
           #this evaluates to e.g. VROT = [20,30,40,50]
           exec(self.gw.par + "= self.gw.getParameter(self.gw.par,self.gw.data)") in globals(), locals()
           
           self.gw.numPrecisionY = self.gw.numPrecision(self.gw.par,self.gw.data)
           
           #this evaluates to the content of the variable in par; e.g. tmp = VROT[:]
           tmp = eval(self.gw.par)
           
           diff = self.gw.NUR[0]-len(tmp)
           lastIndexItem = len(tmp)-1
           if diff == self.gw.NUR[0]:
               for i in range(int(diff)):
                   eval(self.gw.par).append(0.0)
           elif diff > 0 and diff < self.gw.NUR[0]:
               for i in range(int(diff)):
                   eval(self.gw.par).append(tmp[lastIndexItem])
            
           self.gw.parVals[self.gw.par] = eval(self.gw.par)
            
           self.gw.historyList[self.gw.par] = [self.gw.parVals[self.gw.par][:]]
            
            #print (historyList)
           if max(self.gw.parVals[self.gw.par])<=0:
               self.gw.yScale = [-50,50]
           elif (max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par]))<=100:
               self.gw.yScale = [int(ceil(-2*max(self.gw.parVals[self.gw.par]))),int(ceil(2*max(self.gw.parVals[self.gw.par])))]
           else:
               self.gw.yScale = [int(ceil(min(self.gw.parVals[self.gw.par])-0.1*(max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par])))),int(ceil(max(self.gw.parVals[self.gw.par])+0.1*(max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par]))))]
            
           self.gw.key = "Yes"
           self.gw.plotFunc()
           self.ps.close()


def main():
    app = QtGui.QApplication(sys.argv)
#    app.geometry("1280x720")
    GUI = mainWindow()
    GUI.show()
    app.exec_()



if __name__ == '__main__':
    main()