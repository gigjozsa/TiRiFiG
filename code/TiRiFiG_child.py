# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:49:38 2017

@author: samuel

"""

#libraries
#import matplotlib
#matplotlib.use("qt4Agg")
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

from PyQt4 import QtGui, QtCore
import os,sys, threading
from subprocess import Popen as run
from copy import deepcopy
from math import ceil 
import collections


#classes

class GraphWidget(QtGui.QWidget):
    
    key = "Yes"
    ncols = 2; nrows = 2
    currAx = "ax"; plotArea = "par"; ax = "someAxis"
    scaleChange = "No" ; scaleChangeR = 0
    choice = "Beyond Viewgraph"; choiceR = 0
    INSET = 'None'
    par = ['VROT','SBR','INCL','PA']; parR  = 0
    unitMeas = ['km/s','Jy km/s/sqarcs','degrees','degrees']; unitMeasR = 0
    tmpDeffile = os.getcwd() + "/tmpDeffile.def"
    fileName = None
    
    before = 0; beforeR = 0
    numPrecisionY = 0; numPrecisionYR = 0
    numPrecisionX = 0; numPrecisionXR = 0
    NUR = 0;NURR = 0 
    data = []
    parVals = {}; parValsR = 0 
    historyList = {}; historyListR = {}
    historyKeys = [['VROT','km/s',1]]; historyKeysR = [[]]
    historyKeysDup = {'VROT':1}; historyKeysDupR = {}
    xScale=[0,0]; xScaleR=[0,0]
    yScale={'VROT':[0,0]}; yScaleR=[0,0];
    redo = []
       
    
    mPress=[-5]; mPressR = 0
    mRelease=['None']; mReleaseR = 0
    mMotion=[-5]; mMotionR = 0
#    yVal = 0; yValR =0
    
    
    
    
    
    def __init__(self):
        super(GraphWidget, self).__init__()
        #Grid Layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        self.setMinimumSize(1280,720)
        self.center()
        
        #Canvas and Toolbar
        self.figure = plt.figure() 
        
        
        # self.scroll = QtGui.QScrollArea(self)
        # grid.layout(self.scroll)
        self.canvas = FigureCanvas(self.figure)
#        self.toolbar = NavigationToolbar(self.canvas, self)
#        self.canvas = FigureCanvas(self.f)
        self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.canvas.setFocus()
        # self.scroll.setWidget(self.canvas)
        
        
        self.canvas.mpl_connect('button_press_event', self.getClick)
        self.canvas.mpl_connect('button_release_event', self.getRelease)
        self.canvas.mpl_connect('motion_notify_event', self.getMotion)
        self.canvas.mpl_connect('key_press_event', self.keyPressed)
        
#        grid.addWidget(self.toolbar, 1,0,1,2)
#        grid.addWidget(self.canvas, 2,0,1,2)
        
        grid.addWidget(self.canvas, 2,0,1,2)
#        grid.addWidget(self.scroll,1,1)

        #Import def and plot
        btn1 = QtGui.QPushButton('', self)
        btn1.setFixedSize(50,30)
        btn1.setFlat(True)
        btn1.setIcon(QtGui.QIcon('open_folder.png'))
        btn1.setToolTip('Open .def file')
        btn1.clicked.connect(self.openDef)
        grid.addWidget(btn1,0,0)
        
        #Import 2nd .def file and plot
#        btn2 = QtGui.QPushButton('', self)
#        btn2.setFixedSize(50,30) 
#        btn2.setFlat(True)
#        btn2.setIcon(QtGui.QIcon('open_folder2.png'))
#        btn2.setToolTip('Open Underlying .def file')
#        btn2.clicked.connect(self.firstPlot) 
#        grid.addWidget(btn2, 0,1)
            
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
            if os.path.isfile(self.tmpDeffile):
                os.remove(self.tmpDeffile)
            sys.exit(0)
        else:
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

    def strType(self,var):
        """Determines the data type of a variable
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        var  --         variable holding the values
       
        Returns:
        int, float or str : string
        
        The function evaluates the data type of the var object and returns int, 
        float or str
        """        
        try:
            if int(var) == float(var):
                return 'int'
        except:
            try:
                float(var)
                return 'float'
            except:
                return 'str'
             
    def getParameter(self,data):
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

        for i in data:
            lineVals = i.split("=")
            if (len(lineVals)>1):
                lineVals[0] = ''.join(lineVals[0].split())
                #if (sKey == lineVals[0]):
                parVal = lineVals[1].split()

                
                if lineVals[0].upper() == "INSET":
                    self.INSET = ''.join(lineVals[1].split())
                
                if lineVals[0].upper()=="NUR":

                    self.NUR = int(parVal[0])

                else:

                    if (len(parVal)>0) and not(self.strType(parVal[0]) == 'str') and not(self.strType(parVal[-1]) == 'str') and not(self.strType(parVal[len(parVal)/2]) == 'str'):
                        precision = self.numPrecision(parVal)
                        for i in range(len(parVal)):
                            parVal[i]=round(float(parVal[i]),precision)
                        self.parVals[str.upper(lineVals[0])] =  parVal[:] 


    def numPrecision(self,data):
        """Determines and sets floating point precision 
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        data (list) --  list of values of type string e.g. x = ["20.3","55.0003","15.25","12.71717"]
        
        Returns:
        None
        
        Determines the highest floating point precision of data points
        """
        
        decPoints = []
        
        for i in range(len(data)):
               data[i] = str(data[i])
    
        for i in range(len(data)):
            val = data[i].split(".")
            
#            check val has decimal & fractional part and append length of numbers of fractional part
            if len(val)==2:
                decPoints.append(len(val[1]))
        
#        assign greatest precision in decPoints to class variables handling precision

        if len(decPoints)==0:
            return 0
        else:
            return max(decPoints)
            
        
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
            self.getParameter(self.data)
            
            self.numPrecisionY = self.numPrecision(self.parVals['VROT'][:])
            self.numPrecisionX = self.numPrecision(self.parVals['RADI'][:])

#           ensure there are the same points for parameters as there are for RADI as specified in NUR parameter
            for i in range(len(self.par)):

                diff = self.NUR-len(self.parVals[self.par[i]])
                lastItemIndex = len(self.parVals[self.par[i]])-1
                if diff == self.NUR:
                    for j in range(int(diff)):
                        self.parVals[self.par[i]].append(0.0)
                elif diff > 0 and diff < self.NUR:
                    for j in range(int(diff)):
                        self.parVals[self.par[i]].append(self.parVals[self.par[i]][lastItemIndex])
                
            self.historyList.clear()
            for i in self.parVals:
                self.historyList[i] = [self.parVals[i][:]]
            
            #defining the x scale for plotting

            if (max(self.parVals['RADI'])-min(self.parVals['RADI']))<=100:
                self.xScale = [int(ceil(-2*max(self.parVals['RADI']))),int(ceil(2*max(self.parVals['RADI'])))]                           
            else:
                self.xScale = [int(ceil(min(self.parVals['RADI'])-0.1*(max(self.parVals['RADI'])-min(self.parVals['RADI'])))),int(ceil(max(self.parVals['RADI'])+0.1*(max(self.parVals['RADI'])-min(self.parVals['RADI']))))]                            

            # if (max(self.parVals['VROT'])-min(self.parVals['VROT']))<=100:
            #     self.yScale = [int(ceil(-2*max(self.parVals['VROT']))),int(ceil(2*max(self.parVals['VROT'])))]
            # else:
            #     self.yScale = [int(ceil(min(self.parVals['VROT'])-0.1*(max(self.parVals['VROT'])-min(self.parVals['VROT'])))),int(ceil(max(self.parVals['VROT'])+0.1*(max(self.parVals['VROT'])-min(self.parVals['VROT']))))]
            
            
            self.firstPlot()
        
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
        
        # print self.currAx, event.inaxes
        if (event.button == 1) and not(event.xdata == None):
            self.currAx = event.inaxes
            self.mPress[0]=round(float(event.xdata),self.numPrecisionX)
            # print self.mPress[0], round(float(event.ydata),self.numPrecisionY)
#            self.yVal = round(float(event.ydata),self.numPrecisionY)
            self.mRelease[0]=None
        

            
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
#            self.historyKeys[[i for i in range(len(self.historyKeys)-1,-1,-1) if self.historyKeys[i][0] == self.par][0]][2]+=1
        
        #append the new point to the history if the last item in history differs
        #from the new point
        if not(self.historyList[self.par[0]][len(self.historyList[self.par[0]])-1]==self.parVals[self.par[0]][:]):
            self.historyList[self.par[0]].append(self.parVals[self.par[0]][:])
            self.historyKeys[[i for i in range(len(self.historyKeys)-1,-1,-1) if self.historyKeys[i][0] == self.par[0]][0]][2]+=1
            
            self.scaleChangeR = 0; self.choiceR = 0; self.parR  = 0
            self.unitMeasR = 0; self.beforeR = 0; self.numPrecisionYR = 0; self.numPrecisionXR = 0
            self.NURR = 0; self.parValsR = 0; self.historyListR = {}; self.historyKeysR = [[]]
            self.historyKeysDupR = {}; self.xScaleR=[0,0]; self.yScaleR=[0,0]; self.redo = []    
            self.mPressR = 0; self.mReleaseR = 0; self.mMotionR = 0
    
            
        self.mPress[0]=None
      
#                self.mRelease[0]=None


    def getMotion(self,event):
        """Mouse is in motion
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        event --        event type
        
        Returns:
        None
        
        *
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
        
        keyComb = event.key
        
        #comments below may not be that explanatory
         
        #when the key combination Ctrl + z is pressed
        if str.lower(keyComb.encode('ascii','ignore')) == "ctrl+z":
            
            #copy the existing state
            self.scaleChangeR = self.scaleChange
            self.choiceR = self.choice
            self.parR = self.par
            self.unitMeasR = self.unitMeas
            self.beforeR = self.before
            self.numPrecisionXR = self.numPrecisionX
            self.numPrecisionYR = self.numPrecisionY
            self.NURR = self.NUR
            self.parValsR = deepcopy(self.parVals)
            self.historyListR = deepcopy(self.historyList)
            self.historyKeysR = self.historyKeys[:]
            self.historyKeysDupR = deepcopy(self.historyKeysDup)
            self.xScaleR = self.xScale[:]
            self.yScaleR = self.yScale[:]
            self.mMotionR = self.mMotion[:]
            self.mPressR = self.mPress[:]
            self.mReleaseR = self.mRelease[:]
            
            self.redo.append([self.scaleChangeR,self.choiceR,self.parR,
                             self.unitMeasR, self.beforeR,self.numPrecisionXR,
                             self.numPrecisionYR,self.NURR,self.parValsR,
                             self.historyListR,self.historyKeysR,self.historyKeysDupR,
                             self.xScaleR,self.yScaleR,self.mMotionR,self.mPressR,
                             self.mReleaseR])
            
            
            
            #has the user chosen more than one parameter in the viewgraph
            if (len(self.historyKeys)>1):
                
                #has the current parameter been loaded more than once
                if self.historyKeysDup[self.historyKeys[-1][0]] > 1:
                    
                    #is the current duplicate exhausted of points shifted in viewgraph
                    if self.historyKeys[[i for i in range(len(self.historyKeys)-1,-1,-1) if self.historyKeys[i][0] == self.par][0]][2] == 0:
                        #reduce duplicate value of specified parameter by one
                        self.historyKeysDup[self.par]-=1
                        #remove that duplicate entry from the list of loaded parameters
                        self.historyKeys.pop()
                        #set par & unit mesurement to new parameter in last element of historyKeys
                        self.par = self.historyKeys[-1][0]
                        self.unitMeas = self.historyKeys[-1][1]
                        #define the plotting scale
                        if max(self.parVals[self.historyKeys[-1][0]])<=0:
                            self.yScale = [-100,100]
                        elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
                            self.yScale =  [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
                        else:
                            self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                        
                        self.key = "Yes"
                        self.plotFunc()
                    else:
                        #pop the last element(data point from historyList)
                        self.historyList[self.historyKeys[-1][0]].pop()
                        #re-assign parVals to hold points in -1 index of historyList
                        tempHistoryList = self.historyList[self.historyKeys[-1][0]][-1]
                        for i in range(len(self.parVals[self.historyKeys[-1][0]])):
                            self.parVals[self.historyKeys[-1][0]][i]=round(tempHistoryList[i],self.numPrecisionY)
                        
                        #define scale for plotting
                        if max(self.parVals[self.historyKeys[-1][0]])<=0:
                            self.yScale = [-100,100]
                        elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
                            self.yScale =  [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
                        else:
                            self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                    
                        #investigate on using break statement in the list comprehension
                        self.key = "Yes"
                        self.plotFunc()
                        self.historyKeys[[i for i in range(len(self.historyKeys)-1,-1,-1) if self.historyKeys[i][0] == self.par][0]][2]-=1
                                           
                else:#there are no duplicates for this parameter
                    #for that specific parameter, are there many points in history
                    if len(self.historyList[self.historyKeys[-1][0]])>1:
                        #comments same as above
                        self.historyList[self.historyKeys[-1][0]].pop()
                        tempHistoryList = self.historyList[self.historyKeys[-1][0]][-1]
                        #re-assign parVal to hold last list values in history list dictionary
                        #and re-draw graph
                        for i in range(len(self.parVals[self.historyKeys[-1][0]])):
                            self.parVals[self.historyKeys[-1][0]][i]=round(tempHistoryList[i],self.numPrecisionY)
                        if max(self.parVals[self.historyKeys[-1][0]])<=0:
                            self.yScale = [-100,100]
                        elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
                            self.yScale = [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
                        else:
                            self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                        
                        self.key = "Yes"
                        self.plotFunc()
                    else:#there is only one data point for this parameter in history 
                        #comments for code below same as comments above
                        self.historyKeys.pop()
                        self.par = self.historyKeys[-1][0]
                        self.unitMeas = self.historyKeys[-1][1]
    
                        if max(self.parVals[self.historyKeys[-1][0]])<=0:
                            self.yScale = [-100,100]
                        elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
                            self.yScale = [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
                        else:
                            self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                    
                        self.key = "Yes"
                        self.plotFunc()
            else:#only one parameter has been loaded in viewgraph
            
                #only one parameter is in history key and there are more than one point in the historyList for this parameters
                if (len(self.historyKeys)==1) and (len(self.historyList[self.historyKeys[-1][0]])>1):
                    self.historyList[self.historyKeys[-1][0]].pop()
                    tempHistoryList = self.historyList[self.historyKeys[-1][0]][-1]
                    for i in range(len(self.parVals[self.historyKeys[-1][0]])):
                        self.parVals[self.historyKeys[-1][0]][i]=round(tempHistoryList[i],self.numPrecisionY)
                    if max(self.parVals[self.historyKeys[-1][0]])<=0:
                        self.yScale = [-100,100]
                    elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
                        self.yScale = [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
                    else:
                        self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                    
                    self.key = "Yes"
                    self.plotFunc()                    
                else:#number of elements in the history list for last parameter is 1
                #pop up a messageBox saying history list is exhausted
#                
                    self.showInformation()
                    
        elif str.lower(keyComb.encode('ascii','ignore')) == "ctrl+y":
            
         #copy the existing state
            if len(self.redo)>0:
                self.scaleChange = self.redo[-1][0]
                self.choice = self.redo[-1][1]
                self.par = self.redo[-1][2]
                self.unitMeas = self.redo[-1][3]
                self.before= self.redo[-1][4]
                self.numPrecisionX = self.redo[-1][5]
                self.numPrecisionY = self.redo[-1][6]
                self.NUR = self.redo[-1][7]
                self.parVals = deepcopy(self.redo[-1][8])
                self.historyList = deepcopy(self.redo[-1][9])
                self.historyKeys = self.redo[-1][10][:]
                self.historyKeysDup = deepcopy(self.redo[-1][11])
                self.xScale = self.redo[-1][12][:]
                self.yScale = self.redo[-1][13][:]
                self.mMotion = self.redo[-1][14][:]
                self.mPress = self.redo[-1][15][:]
                self.mRelease = self.redo[-1][16][:]
            
                self.redo.pop()
                self.key="Yes"
                self.plotFunc() 
            else:
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
        self.ax = [None] * (self.nrows * self.ncols)
        counter = 0
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j))
                counter+=1
        # if ((self.nrows + self.ncols) % 2 == 0):
        #     for i in range(self.nrows):
        #         for j in range(self.ncols):
        #             ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j))
        #             counter+=1
        # else:
        #     for i in range(self.rows):
        #         for j in range(self.cols):
        #             if (i == self.nrows -1) and (j == self.ncols-1):
        #                 ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j), colspan=self.ncols)
        #             else:
        #                 ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j))
        #             counter+=1

        # # ax = self.figure.add_subplot(221)
        # ax = plt.subplot2grid((2, 2), (0, 0))
        # ax2 = plt.subplot2grid((2, 2), (0, 1))
        # ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

        for i in range(len(self.par)):
            self.ax[i].clear()
            self.ax[i].set_xlim(self.xScale[0],self.xScale[1])
#            if (max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))<=100:
#                self.yScale[self.par[i]] = [int(ceil(-2*max(self.parVals[self.par[i]]))),int(ceil(2*max(self.parVals[self.par[i]])))]
#            else:
#                self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
            if self.choice == "Beyond Viewgraph":
                if (max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))<=100:
                    self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
                else:
                    self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
            elif self.choice == "Free":
                if (max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))<=100:
                    self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par])-min(self.parVals[self.par[i]]))))]
                else:
                    self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
         
                      
            self.ax[i].set_ylim(self.yScale[self.par[i]][0],self.yScale[self.par[i]][1])
       
        

            # for axes in self.figure.get_axes():
            #     axes.set_xlabel("RADI (arcsec)")
            #     axes.set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")
            self.ax[i].set_xlabel("RADI (arcsec)")
            self.ax[i].set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")

            self.ax[i].plot(self.parVals['RADI'], self.historyList[self.par[i]][len(self.historyList[self.par[i]])-1],'--bo')
            self.ax[i].set_title('Plot')
            self.ax[i].set_xticks(self.parVals['RADI'])
#        ax.set_yticks(np.arange(min(self.parVals[self.par]),max(self.parVals[self.par])+1,500))
        plt.tight_layout()
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
        for i in range(len(self.ax)):
#            print self.ax[i], self.currAx
#            print "ax[%d] == self.currAx: "%(i),self.ax[i].axes == self.currAx.axes
            if self.ax[i] ==  self.currAx:
                self.plotArea = self.par[i]
                
        i = self.par.index(self.plotArea)       
#        ax = [None] * (self.nrows * self.ncols)
#        counter = 0
#        for i in range(self.nrows):
#            for j in range(self.ncols):
#                ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j))
#                print ax[counter], self.currAx
#                print "ax[%d] == self.currAx: "%(counter),ax[counter].axes == self.currAx.axes

#                if ax[counter] == self.currAx:
#                    self.plotArea = self.par[counter]
#                counter+=1


        if self.scaleChange == "Yes":
            # ax = self.figure.add_subplot(111)
            # if ((self.nrows + self.ncols) % 2 == 0):
            #     for i in range(self.nrows):
            #         for j in range(self.ncols):
            #             ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j))
            #             counter+=1
            # else:
            #     for i in range(self.rows):
            #         for j in range(self.cols):
            #             if (i == self.nrows -1) and (j == self.ncols-1):
            #                 ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j), colspan=ncols)
            #             else:
            #                 ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j))
            #             counter+=1
            # ax = plt.subplot2grid((nrows, ncols), (0, 0))
            # ax2 = plt.subplot2grid((nrows, ncols), (0, 1))
            # ax3 = plt.subplot2grid((nrows, ncols), (1, 0), colspan=2)
            # print ax
            for i in range(len(self.par)):
                self.ax[i].clear()
                self.ax[i].set_xlim(self.xScale[0],self.xScale[1])
                if (max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))<=100:
                    self.yScale[self.par[i]] = [int(ceil(-2*max(self.parVals[self.par[i]]))),int(ceil(2*max(self.parVals[self.par[i]])))]
                else:
                    self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
                          
                self.ax[i].set_ylim(self.yScale[self.par[i]][0],self.yScale[self.par[i]][1])
           
            

                # for axes in self.figure.get_axes():
                #     axes.set_xlabel("RADI (arcsec)")
                #     axes.set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")
                self.ax[i].set_xlabel("RADI (arcsec)")
                self.ax[i].set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")

                self.ax[i].plot(self.parVals['RADI'], self.historyList[self.par[i]][len(self.historyList[self.par[i]])-1],'--bo')
#                self.ax[i].set_title('Plot')
                self.ax[i].set_xticks(self.parVals['RADI'])


            plt.tight_layout()
            self.canvas.draw()
            self.key = "No"
        

        if self.key=="Yes":
            self.firstPlot()
            
        #this re-plots the graph as long as the mouse is in motion and the right data point is clicked
        else:
            for j in range(len(self.parVals['RADI'])):
                if (self.mPress[0] < (self.parVals['RADI'][j])+3) and (self.mPress[0] > (self.parVals['RADI'][j])-3) and (self.mRelease[0]==None):
                    
#                    print "before: ", self.parVals[self.plotArea][j]
                    self.parVals[self.plotArea][j] = self.mMotion[0]
#                    print "after: ",self.parVals[self.plotArea][j]

                    # if ((self.nrows + self.ncols) % 2 == 0):
                    #     for i in range(self.nrows):
                    #         for j in range(self.ncols):
                    #             ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j))
                    #             counter+=1
                    # else:
                    #     for i in range(self.rows):
                    #         for j in range(self.cols):
                    #             if (i == self.nrows -1) and (j == self.ncols-1):
                    #                 ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j), colspan=self.ncols)
                    #             else:
                    #                 ax[counter] = plt.subplot2grid((self.nrows, self.ncols), (i, j))
                    #             counter+=1
                    # ax = self.figure.add_subplot(111)
                    # ax = plt.subplot2grid((2, 2), (0, 0))
                    # ax2 = plt.subplot2grid((2, 2), (0, 1))
                    # ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2) 
        #            for i in range(len(self.par)):
                    self.ax[i].clear()
                    self.ax[i].set_xlim(self.xScale[0],self.xScale[1])
        
                    if self.choice == "Beyond Viewgraph":
        
                        if self.mMotion[0] >= 0.85*self.yScale[self.par[i]][1]:
                            
                            self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
        
                        elif abs(self.mMotion[0]) <= abs(1.15*self.yScale[self.par[i]][0]):
                            self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
                            
        #                            self.yScale[0] -= (self.yScale[0]*0.5) if self.yScale[0]>0 else (self.yScale[0]*-0.5)
        #                            self.yScale[1] += (self.yScale[1]*0.5) if self.yScale[1]>0 else (self.yScale[1]*-0.5)
                        
                    elif self.choice == "Free":
                        if (max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))<=100:
                            self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
                            
        #                            self.yScale = [int(ceil(-2*max(self.parVals[self.par]))),int(ceil(2*max(self.parVals[self.par])))]
                        else:
                            self.yScale[self.par[i]] = [int(ceil(min(self.parVals[self.par[i]])-0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]])))),int(ceil(max(self.parVals[self.par[i]])+0.1*(max(self.parVals[self.par[i]])-min(self.parVals[self.par[i]]))))]
                    
                    print self.yScale[self.par[i]]
                    
                    self.ax[i].set_ylim(self.yScale[self.par[i]][0],self.yScale[self.par[i]][1])
                    
                
        
                    # for axes in self.figure.get_axes():
                    #     axes.set_xlabel("RADI (arcsec)")
                    #     axes.set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")
                    self.ax[i].set_xlabel("RADI (arcsec)")
                    self.ax[i].set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")
        
                    self.ax[i].plot(self.parVals['RADI'], self.historyList[self.par[i]][len(self.historyList[self.par[i]])-1],'--bo')
        #            self.ax[i].set_title('Plot')
                    self.ax[i].set_xticks(self.parVals['RADI'])
        
        
                    plt.tight_layout()
                    self.canvas.draw()
                    self.key = "No"              

    
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
        #instead of specific precision, call precision function for each param
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
        
        self.saveMessage()
    
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
    
    def saveAsMessage(self):
        """Displays the information about save action
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Displays a messagebox that informs user that changes have been successfully written to the .def file
        """
        QtGui.QMessageBox.information(self, "Information", "File Successfully Saved")
        
        
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
            
        self.saveAsMessage()
        
            
    def tirificMessage(self):
        """Displays the information about save action
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Displays a messagebox that informs user that changes have been successfully written to the .def file
        """
        QtGui.QMessageBox.information(self, "Information", "Data cube ("+self.INSET+") specified at INSET doesn't exist in current working directory.")
        
    
    def startTiriFiC(self):
        """Start TiRiFiC
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of 
        the mainWindow class
        
        Returns:
        None
        
        Calls the os.system and opens terminal to start TiRiFiC
        """
        fileName = os.getcwd()
        fileName = fileName+"/"+self.INSET
        if os.path.isfile(fileName):
            for i in self.parVals:
                self.saveFile(self.parVals[i],i)
            os.system("gnome-terminal -e 'bash -c \"/home/samuel/software/TiRiFiC/tirific_2.3.4/bin/tirific deffile = "+self.fileName+"; exec bash\"'")
        else:
            self.tirificMessage()
        
        
    def slotChangeData(self,fileName):

        with open(fileName) as f:
            self.data = f.readlines()
        f.close()
        

        self.getParameter(self.data)

        self.numPrecisionY = self.numPrecision(self.parVals[self.par][:])
        self.numPrecisionX = self.numPrecision(self.parVals['RADI'][:])
        
#        ensure there are the same points for parameter as there are for RADI as specified in NUR parameter
#        diff = self.NUR-len(self.parVals[self.par])
#        lastItemIndex = len(self.parVals[self.par])-1
#        if diff == self.NUR:
#            for i in range(int(diff)):
#                self.parVals[self.par].append(0.0)
#        elif diff > 0 and diff < self.NUR:
#            for i in range(int(diff)):
#                self.parVals[self.par].append(self.parVals[self.par][lastItemIndex])
        
        for i in self.parVals:
#                self.saveFile(self.parVals[i],i)
            if not(self.historyList[i][len(self.historyList[i])-1]==self.parVals[i][:]):
                self.historyList[i].append(self.parVals[i][:])
#        self.historyList.clear()
#        for i in self.parVals:
#            self.historyList[i] = [self.parVals[i][:]]
            
        #defining the x and y scale for plotting
        if (max(self.parVals['RADI'])-min(self.parVals['RADI']))<=100:
            self.xScale = [int(ceil(-2*max(self.parVals['RADI']))),int(ceil(2*max(self.parVals['RADI'])))]                           
        else:
            self.xScale = [int(ceil(min(self.parVals['RADI'])-0.1*(max(self.parVals['RADI'])-min(self.parVals['RADI'])))),int(ceil(max(self.parVals['RADI'])+0.1*(max(self.parVals['RADI'])-min(self.parVals['RADI']))))]                            

        if (max(self.parVals[self.par])-min(self.parVals[self.par]))<=100:
            self.yScale = [int(ceil(-2*max(self.parVals[self.par]))),int(ceil(2*max(self.parVals[self.par])))]
        else:
            self.yScale = [int(ceil(min(self.parVals[self.par])-0.1*(max(self.parVals[self.par])-min(self.parVals[self.par])))),int(ceil(max(self.parVals[self.par])+0.1*(max(self.parVals[self.par])-min(self.parVals[self.par]))))] 
        self.firstPlot()
        
    def animate(self):
        fileName = os.getcwd()
        fileName += "/tmpDeffile.def"
        

        if os.path.isfile(self.tmpDeffile):
            
            after = os.stat(self.tmpDeffile).st_mtime
            if self.before != after:
                self.before = after
                self.slotChangeData(self.tmpDeffile)
        else:
            pass
        
        t = threading.Timer(1.0, self.animate)
        t.daemon = True
        t.start()
        
        
    def openEditor(self):
        text,ok = QtGui.QInputDialog.getText(self,'Text Editor Input Dialog', 
                                            'Enter text editor:')
                                            
        if ok:

            for i in self.parVals:
                self.saveAs(self.tmpDeffile,self.parVals[i],i)

            if len(text)>0:
                programName = str(text)
                run([programName,self.tmpDeffile])
            else:
                run(["gedit",self.tmpDeffile])  
                
#            assign current modified time of temporary def file to before    
            self.before = os.stat(self.tmpDeffile).st_mtime

    def setRowCol(self):
         text,ok = QtGui.QInputDialog.getText(self,'Window number Input Dialog', 
                                            'Specify the number of rows and columns (5,5):')

         if ok:
            print "ok was clicked"
            if len(text) > 0:

                text = str(text)
                text = text.split(",")

                self.nrows = int(text[0])
                self.ncols = int(text[1])
                self.firstPlot()


    

class SMWindow(QtGui.QWidget):

    def __init__(self,xMinVal,xMaxVal,yMinVal,yMaxVal,par):
        super(SMWindow, self).__init__()
        self.xMinVal = xMinVal
        self.xMaxVal = xMaxVal
        self.yMinVal = yMinVal
        self.yMaxVal = yMaxVal
        self.par = par


        self.xMin = QtGui.QLineEdit()
        self.xMin.minimumSize()
        self.xMin.setPlaceholderText("RADI min ("+str(self.xMinVal)+")")        
        self.xMax = QtGui.QLineEdit()
        self.xMax.minimumSize()
        self.xMax.setPlaceholderText("RADI max ("+str(self.xMaxVal)+")")  
       
        self.yMin = QtGui.QLineEdit()
        self.yMin.minimumSize()
        self.yMin.setPlaceholderText(self.par+" min ("+str(self.yMinVal)+")")
        self.yMax = QtGui.QLineEdit()
        self.yMax.minimumSize()
        self.yMax.setPlaceholderText(self.par+" max ("+str(self.yMaxVal)+")")
    
    
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

        self.sm = SMWindow(self.gw.xScale[0],self.gw.xScale[1],self.gw.yScale[self.gw.par[0]][0],self.gw.yScale[self.gw.par[0]][1],self.gw.par[0])
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

        self.winSpec = QtGui.QAction("&Window Specification",self)
        self.winSpec.setStatusTip('Determines the number of rows and columns in a plot')
        self.winSpec.triggered.connect(self.gw.setRowCol)

        self.scaleMan = QtGui.QAction("&Scale Manager",self)
        self.scaleMan.setStatusTip('Manages behaviour of scale and min and max values')
        self.scaleMan.triggered.connect(self.reloadSM)
        
        self.paraDef = QtGui.QAction("&Parameter Definition",self)
        self.paraDef.setStatusTip('Determines which parameter is plotted on the y-axis')
        self.paraDef.triggered.connect(self.ps.show)
        
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
        self.prefMenu.addAction(self.winSpec)
        
    def reloadSM(self):
        self.sm = SMWindow(self.gw.xScale[0],self.gw.xScale[1],self.gw.yScale[0],self.gw.yScale[1],self.gw.par)
        self.sm.show()
        self.sm.radioFree.clicked.connect(self.getOptF)
        self.sm.radioViewG.clicked.connect(self.getOptV)
        self.sm.btnUpdate.clicked.connect(self.updateScale)
        self.sm.btnCancel.clicked.connect(self.sm.close)
        self.ps.btnOK.clicked.connect(self.paramDef)
        self.ps.btnCancel.clicked.connect(self.close)
    
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
       
       if len(self.ps.parameter.text())>0 and not(str.upper(str(self.ps.parameter)) == str.upper(self.gw.par)):
           self.gw.par = str.upper(str(self.ps.parameter.text()))
           self.gw.unitMeas = str(self.ps.unitMeasurement.text())
           
           if self.gw.par in self.gw.parVals:
               self.gw.numPrecisionY = self.gw.numPrecision(self.gw.parVals[self.gw.par][:])
               diff = self.gw.NUR-len(self.gw.parVals[self.gw.par])
               if diff == self.gw.NUR:
                   for i in range(diff):
                       self.gw.parVals[self.gw.par].append(0.0)
               elif diff > 0 and diff < self.gw.NUR:
                   for i in range(diff):
                       self.gw.parVals[self.gw.par].append(self.gw.parVals[self.gw.par][-1])
           else:
               zeroVals = []
               self.gw.numPrecisionY = 1
               for i in range(self.gw.NUR):
                   zeroVals.append(0.0)
               self.gw.parVals[self.gw.par] = zeroVals[:]
               
               
           #if the parameter specified is not in parVals, then obviously it isnt in historyList
           #therefore there's no need for another if statement here
           #evaluate the statements in the if-else condition above
           if self.gw.par in self.gw.historyList:
               if (len(self.gw.historyList[self.gw.par])<1) or ((len(self.gw.historyList[self.gw.par])>0) and not(self.gw.historyList[self.gw.par][-1]==self.gw.parVals[self.gw.par][:])):
                   self.gw.historyList[self.gw.par].append(self.gw.parVals[self.gw.par][:])
    
           else:
               self.gw.historyList[self.gw.par] = [self.gw.parVals[self.gw.par][:]]
            
           if max(self.gw.parVals[self.gw.par])<=0:
               self.gw.yScale = [-100,100]
           elif (max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par]))<=100:
               self.gw.yScale = [int(ceil(-2*max(self.gw.parVals[self.gw.par]))),int(ceil(2*max(self.gw.parVals[self.gw.par])))]
           else:
               self.gw.yScale = [int(ceil(min(self.gw.parVals[self.gw.par])-0.1*(max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par])))),int(ceil(max(self.gw.parVals[self.gw.par])+0.1*(max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par]))))]
           
           if self.gw.par in [self.gw.historyKeys[i][0] for i in range(len(self.gw.historyKeys))]:
               self.gw.historyKeys.append([self.gw.par,self.gw.unitMeas,0])
           else:
               self.gw.historyKeys.append([self.gw.par,self.gw.unitMeas,1])
           self.gw.historyKeysDup = collections.Counter([self.gw.historyKeys[i][0] for i in range(len(self.gw.historyKeys))])
           self.gw.key = "Yes"
           self.gw.plotFunc()
           self.ps.close()

def main():
    if os.path.isfile(os.getcwd() + "/tmpDeffile.def"):
        os.remove(os.getcwd() + "/tmpDeffile.def")

    app = QtGui.QApplication(sys.argv)
    GUI = mainWindow()
    GUI.show()

    try:
        GUI.gw.animate()
    except SystemExit:
        print "Done"

    app.exec_()


if __name__ == '__main__':
    main()
