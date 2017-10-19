# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:49:38 2017

@author: samuel

This script here is the GUI (PyQt) implementation of TiRiFiC. As of now the code has been
written in Python 3. Future considerations would be made to have it run on Python 2.7 as
well.

functions:
    main 

This needs revision
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

#libraries
#import matplotlib
#matplotlib.use("qt4Agg")
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

from PyQt4 import QtGui, QtCore
import os,sys, threading
from subprocess import Popen as run
from copy import deepcopy
from math import ceil 
import collections
import numpy as np

currPar = "none"

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
    

class TimerThread():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = threading.Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = threading.Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

        
class GraphWidget(QtGui.QWidget):

    scaleChange = "No" 
   
    mPress=[None,None]
    mRelease=[None,None]
    mMotion=[None]
    mDblPress=[None,None]
    
    
       
    
    def __init__(self,parent,xScale,yScale,choice,unitMeas,par,parVals,parValRADI,historyList,key,numPrecisionX,numPrecisionY):
        super(GraphWidget, self).__init__(parent)
        self.xScale = xScale
        self.yScale = yScale
        self.choice = choice
        self.unitMeas = unitMeas
        self.par = par
        self.parVals = parVals
        self.parValRADI = parValRADI
        self.historyList = historyList
        self.key = key
        self.numPrecisionX = numPrecisionX
        self.numPrecisionY = numPrecisionY
#        self.parValsCopy = []
        
#        print "now in GraphWidget"
#        print self.xScale,self.yScale,self.choice,self.unitMeas,self.par,self.key
        #Grid Layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        
#        self.setMinimumSize(800,600)   

#        self.center()       
        #Canvas and Toolbar
        self.figure = plt.figure() 

        self.canvas = FigureCanvas(self.figure)

#        self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
#        self.canvas.setFocusPolicy( QtCore.Qt.WheelFocus )
        self.canvas.setFocus()
        
        
        self.canvas.mpl_connect('button_press_event', self.getClick)
        self.canvas.mpl_connect('button_release_event', self.getRelease)
        self.canvas.mpl_connect('motion_notify_event', self.getMotion)
        self.canvas.mpl_connect('key_press_event', self.keyPressed)
        
        self.ax = self.figure.add_subplot(111)

        #change the parameter in the viewgraph
        self.btn1 = QtGui.QPushButton('', self)
        self.btn1.setFixedSize(50,30)
        self.btn1.setFlat(True)
        self.btn1.setIcon(QtGui.QIcon('plus.png'))
        self.btn1.setToolTip('Add Parameter')

        #modify plotted parameter
        self.btn2 = QtGui.QPushButton('', self)
        self.btn2.setFixedSize(50,30) 
        self.btn2.setFlat(True)
        self.btn2.setIcon(QtGui.QIcon('edit.png'))
        self.btn2.setToolTip('Modify plotted parameter')
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)
        
        grid.addLayout(hbox,0,0)        
        grid.addWidget(self.canvas, 2,0,1,2) # perhaps you should put this on  row 1 instead of row 2

        
        self.firstPlot()

    
    def changeGlobal(self):
        global currPar
        currPar = self.par
        print currPar
        
        
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
#        print "clicked", event.button

        
        if (event.button == 1) and not(event.xdata == None):
            
             self.mPress[0]=round(float(event.xdata),self.numPrecisionX)
             print self.mPress[0]
             self.mPress[1]=round(float(event.ydata),self.numPrecisionY)
             # print self.mPress[0], round(float(event.ydata),self.numPrecisionY)
 #            self.yVal = round(float(event.ydata),self.numPrecisionY)
             self.mRelease[0]=None
             self.mRelease[1]=None
#             self.parValsCopy = self.parVals[:]
        
        if event.dblclick and not(event.xdata == None):
            self.mDblPress[0] = round(float(event.xdata),self.numPrecisionX)
            self.mDblPress[1] = round(float(event.ydata),self.numPrecisionY)  
            
            text,ok = QtGui.QInputDialog.getText(self,'Input Dialog', 
                                            'Enter new node value:')
                                            
            if ok:
    
                if len(text)>0:
                    newVal = int(str(text))
                    for j in range(len(self.parValRADI)):
                        if (self.mDblPress[0] < (self.parValRADI[j])+3) and (self.mDblPress[0] > (self.parValRADI[j])-3): #and (self.mDblPress[1] < (self.parVals[j])+3) and (self.mDblPress[1] > self.parVals[j])-3):

                            self.parVals[j] = newVal
       
                            self.ax.clear()
                            self.ax.set_xlim(self.xScale[0],self.xScale[1])
                
                            if self.choice == "Beyond Viewgraph":
                               
                                if newVal >= 0.85*self.yScale[1]:
        #                            if np.subtract(max(self.parVals[i]),min(self.parVals[i]))==0:
        #                                self.yScale = 
                                    
                                    self.yScale = [int(ceil(min(self.parVals)-0.1*(max(self.parVals)-min(self.parVals)))),int(ceil(max(self.parVals)+0.1*(max(self.parVals)-min(self.parVals))))]
                
                                elif abs(newVal) <= abs(1.15*self.yScale[0]):
                                    
                                    self.yScale = [int(ceil(min(self.parVals)-0.1*(max(self.parVals)-min(self.parVals)))),int(ceil(max(self.parVals)+0.1*(max(self.parVals)-min(self.parVals))))]
                                    
                 #                            self.yScale[0] -= (self.yScale[0]*0.5) if self.yScale[0]>0 else (self.yScale[0]*-0.5)
                 #                            self.yScale[1] += (self.yScale[1]*0.5) if self.yScale[1]>0 else (self.yScale[1]*-0.5)
                                
                            elif self.choice == "Free":
                                if (max(self.parVals)-min(self.parVals))<=100:
                                    
                                    self.yScale = [int(ceil(min(self.parVals)-0.1*(max(self.parVals)-min(self.parVals)))),int(ceil(max(self.parVals)+0.1*(max(self.parVals)-min(self.parVals))))]
                                    
                 #                            self.yScale = [int(ceil(-2*max(self.parVals[self.par]))),int(ceil(2*max(self.parVals[self.par])))]
                                else:
                                    self.yScale = [int(ceil(min(self.parVals)-0.1*(max(self.parVals)-min(self.parVals)))),int(ceil(max(self.parVals)+0.1*(max(self.parVals)-min(self.parVals))))]
                            
                            
                            self.ax.set_ylim(self.yScale[0],self.yScale[1])
                            
                        
                
                            # for axes in self.figure.get_axes():
                            #     axes.set_xlabel("RADI (arcsec)")
                            #     axes.set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")
                            self.ax.set_xlabel("RADI (arcsec)")
                            self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                            
                
        #                    self.ax.plot(self.parVals['RADI'], self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
                            self.ax.plot(self.parValRADI, self.parVals,'--bo')
                 #           self.ax[i].set_title('Plot')
                            self.ax.set_xticks(self.parValRADI)
                
                
                            plt.tight_layout()
                            self.canvas.draw()
                            self.key = "No"  
                            break
        

            
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

            
             self.mRelease[0]=round(float(event.xdata),self.numPrecisionX)
             self.mRelease[1]=round(float(event.ydata),self.numPrecisionY)
 #            self.historyKeys[[i for i in range(len(self.historyKeys)-1,-1,-1) if self.historyKeys[i][0] == self.par][0]][2]+=1
        
#        append the new point to the history if the last item in history differs
#        from the new point
        if not(self.historyList[len(self.historyList)-1]==self.parVals[:]):
            self.historyList.append(self.parVals[:])
#            self.historyKeys[[i for i in range(len(self.historyKeys)-1,-1,-1) if self.historyKeys[i][0] == self.par][0]][2]+=1
            
#             self.scaleChangeR = 0; self.choiceR = 0; self.parR  = 0
#             self.unitMeasR = 0; self.beforeR = 0; self.numPrecisionYR = 0; self.numPrecisionXR = 0
#             self.NURR = 0; self.parValsR = 0; self.historyListR = {}; self.historyKeysR = [[]]
#             self.historyKeysDupR = {}; self.xScaleR=[0,0]; self.yScaleR=[0,0]; self.redo = []    
#             self.mPressR = 0; self.mReleaseR = 0; self.mMotionR = 0
#    
            
        self.mPress[0]=None
        self.mPress[1]=None
#        self.parValsCopy = []
#      
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
            
#            print event.button
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
#         if str.lower(keyComb.encode('ascii','ignore')) == "ctrl+z":
            
#             #copy the existing state
#             self.scaleChangeR = self.scaleChange
#             self.choiceR = self.choice
#             self.parR = self.par
#             self.unitMeasR = self.unitMeas
#             self.beforeR = self.before
#             self.numPrecisionXR = self.numPrecisionX
#             self.numPrecisionYR = self.numPrecisionY
#             self.NURR = self.NUR
#             self.parValsR = deepcopy(self.parVals)
#             self.historyListR = deepcopy(self.historyList)
#             self.historyKeysR = self.historyKeys[:]
#             self.historyKeysDupR = deepcopy(self.historyKeysDup)
#             self.xScaleR = self.xScale[:]
#             self.yScaleR = self.yScale[:]
#             self.mMotionR = self.mMotion[:]
#             self.mPressR = self.mPress[:]
#             self.mReleaseR = self.mRelease[:]
            
#             self.redo.append([self.scaleChangeR,self.choiceR,self.parR,
#                              self.unitMeasR, self.beforeR,self.numPrecisionXR,
#                              self.numPrecisionYR,self.NURR,self.parValsR,
#                              self.historyListR,self.historyKeysR,self.historyKeysDupR,
#                              self.xScaleR,self.yScaleR,self.mMotionR,self.mPressR,
#                              self.mReleaseR])
            
            
            
#             #has the user chosen more than one parameter in the viewgraph
#             if (len(self.historyKeys)>1):
                
#                 #has the current parameter been loaded more than once
#                 if self.historyKeysDup[self.historyKeys[-1][0]] > 1:
                    
#                     #is the current duplicate exhausted of points shifted in viewgraph
#                     if self.historyKeys[[i for i in range(len(self.historyKeys)-1,-1,-1) if self.historyKeys[i][0] == self.par][0]][2] == 0:
#                         #reduce duplicate value of specified parameter by one
#                         self.historyKeysDup[self.par]-=1
#                         #remove that duplicate entry from the list of loaded parameters
#                         self.historyKeys.pop()
#                         #set par & unit mesurement to new parameter in last element of historyKeys
#                         self.par = self.historyKeys[-1][0]
#                         self.unitMeas = self.historyKeys[-1][1]
#                         #define the plotting scale
#                         if max(self.parVals[self.historyKeys[-1][0]])<=0:
#                             self.yScale = [-100,100]
#                         elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
#                             self.yScale =  [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
#                         else:
#                             self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                        
#                         self.key = "Yes"
#                         self.plotFunc()
#                     else:
#                         #pop the last element(data point from historyList)
#                         self.historyList[self.historyKeys[-1][0]].pop()
#                         #re-assign parVals to hold points in -1 index of historyList
#                         tempHistoryList = self.historyList[self.historyKeys[-1][0]][-1]
#                         for i in range(len(self.parVals[self.historyKeys[-1][0]])):
#                             self.parVals[self.historyKeys[-1][0]][i]=round(tempHistoryList[i],self.numPrecisionY)
                        
#                         #define scale for plotting
#                         if max(self.parVals[self.historyKeys[-1][0]])<=0:
#                             self.yScale = [-100,100]
#                         elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
#                             self.yScale =  [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
#                         else:
#                             self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                    
#                         #investigate on using break statement in the list comprehension
#                         self.key = "Yes"
#                         self.plotFunc()
#                         self.historyKeys[[i for i in range(len(self.historyKeys)-1,-1,-1) if self.historyKeys[i][0] == self.par][0]][2]-=1
                                           
#                 else:#there are no duplicates for this parameter
#                     #for that specific parameter, are there many points in history
#                     if len(self.historyList[self.historyKeys[-1][0]])>1:
#                         #comments same as above
#                         self.historyList[self.historyKeys[-1][0]].pop()
#                         tempHistoryList = self.historyList[self.historyKeys[-1][0]][-1]
#                         #re-assign parVal to hold last list values in history list dictionary
#                         #and re-draw graph
#                         for i in range(len(self.parVals[self.historyKeys[-1][0]])):
#                             self.parVals[self.historyKeys[-1][0]][i]=round(tempHistoryList[i],self.numPrecisionY)
#                         if max(self.parVals[self.historyKeys[-1][0]])<=0:
#                             self.yScale = [-100,100]
#                         elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
#                             self.yScale = [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
#                         else:
#                             self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                        
#                         self.key = "Yes"
#                         self.plotFunc()
#                     else:#there is only one data point for this parameter in history 
#                         #comments for code below same as comments above
#                         self.historyKeys.pop()
#                         self.par = self.historyKeys[-1][0]
#                         self.unitMeas = self.historyKeys[-1][1]
    
#                         if max(self.parVals[self.historyKeys[-1][0]])<=0:
#                             self.yScale = [-100,100]
#                         elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
#                             self.yScale = [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
#                         else:
#                             self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                    
#                         self.key = "Yes"
#                         self.plotFunc()
#             else:#only one parameter has been loaded in viewgraph
            
#                 #only one parameter is in history key and there are more than one point in the historyList for this parameters
#                 if (len(self.historyKeys)==1) and (len(self.historyList[self.historyKeys[-1][0]])>1):
#                     self.historyList[self.historyKeys[-1][0]].pop()
#                     tempHistoryList = self.historyList[self.historyKeys[-1][0]][-1]
#                     for i in range(len(self.parVals[self.historyKeys[-1][0]])):
#                         self.parVals[self.historyKeys[-1][0]][i]=round(tempHistoryList[i],self.numPrecisionY)
#                     if max(self.parVals[self.historyKeys[-1][0]])<=0:
#                         self.yScale = [-100,100]
#                     elif (max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))<=100:
#                         self.yScale = [int(ceil(-2*max(self.parVals[self.historyKeys[-1][0]]))),int(ceil(2*max(self.parVals[self.historyKeys[-1][0]])))]
#                     else:
#                         self.yScale = [int(ceil(min(self.parVals[self.historyKeys[-1][0]])-0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]])))),int(ceil(max(self.parVals[self.historyKeys[-1][0]])+0.1*(max(self.parVals[self.historyKeys[-1][0]])-min(self.parVals[self.historyKeys[-1][0]]))))]
                    
#                     self.key = "Yes"
#                     self.plotFunc()                    
#                 else:#number of elements in the history list for last parameter is 1
#                 #pop up a messageBox saying history list is exhausted
# #                
#                     self.showInformation()
                    
#         elif str.lower(keyComb.encode('ascii','ignore')) == "ctrl+y":
            
#          #copy the existing state
#             if len(self.redo)>0:
#                 self.scaleChange = self.redo[-1][0]
#                 self.choice = self.redo[-1][1]
#                 self.par = self.redo[-1][2]
#                 self.unitMeas = self.redo[-1][3]
#                 self.before= self.redo[-1][4]
#                 self.numPrecisionX = self.redo[-1][5]
#                 self.numPrecisionY = self.redo[-1][6]
#                 self.NUR = self.redo[-1][7]
#                 self.parVals = deepcopy(self.redo[-1][8])
#                 self.historyList = deepcopy(self.redo[-1][9])
#                 self.historyKeys = self.redo[-1][10][:]
#                 self.historyKeysDup = deepcopy(self.redo[-1][11])
#                 self.xScale = self.redo[-1][12][:]
#                 self.yScale = self.redo[-1][13][:]
#                 self.mMotion = self.redo[-1][14][:]
#                 self.mPress = self.redo[-1][15][:]
#                 self.mRelease = self.redo[-1][16][:]
            
#                 self.redo.pop()
#                 self.key="Yes"
#                 self.plotFunc() 
#             else:
#                 self.showInformation()
                             
                             
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
#        ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.set_xlim(self.xScale[0],self.xScale[1])
        self.ax.set_ylim(self.yScale[0],self.yScale[1])
        self.ax.set_xlabel("RADI (arcsec)")
        self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")

        self.ax.plot(self.parValRADI, self.historyList[len(self.historyList)-1],'--bo')
        self.ax.set_title('Plot')
        self.ax.set_xticks(self.parValRADI)
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

        if self.scaleChange == "Yes":

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
     #               self.ax[i].set_title('Plot')
                self.ax[i].set_xticks(self.parVals['RADI'])


            plt.tight_layout()
            self.canvas.draw()
            self.key = "No"
        

        if self.key=="Yes":
            self.firstPlot()
            
        #this re-plots the graph as long as the mouse is in motion and the right data point is clicked
        else:
#            counter = 0
           
            
            for j in range(len(self.parValRADI)):
                if (self.mPress[0] < (self.parValRADI[j])+3) and (self.mPress[0] > (self.parValRADI[j])-3) and (self.mRelease[0]==None): #and (self.mPress[1] < (self.parVals[j])+3) and (self.mPress[1] > (self.parVals[j])-3):
#                    print self.parVals[self.par][j]
 #                   print "before: ", self.parVals[self.plotArea][j]
                    self.parVals[j] = self.mMotion[0]
#                    self.mPress[1] = self.mMotion[0]
                    

#                    self.ax = self.figure.add_subplot(111)
                    self.ax.clear()
                    self.ax.set_xlim(self.xScale[0],self.xScale[1])
        
                    if self.choice == "Beyond Viewgraph":
                       
                        if self.mMotion[0] >= 0.85*self.yScale[1]:
#                            if np.subtract(max(self.parVals[i]),min(self.parVals[i]))==0:
#                                self.yScale = 
                            
                            self.yScale = [int(ceil(min(self.parVals)-0.1*(max(self.parVals)-min(self.parVals)))),int(ceil(max(self.parVals)+0.1*(max(self.parVals)-min(self.parVals))))]
        
                        elif abs(self.mMotion[0]) <= abs(1.15*self.yScale[0]):
                            
                            self.yScale = [int(ceil(min(self.parVals)-0.1*(max(self.parVals)-min(self.parVals)))),int(ceil(max(self.parVals)+0.1*(max(self.parVals)-min(self.parVals))))]
                            
         #                            self.yScale[0] -= (self.yScale[0]*0.5) if self.yScale[0]>0 else (self.yScale[0]*-0.5)
         #                            self.yScale[1] += (self.yScale[1]*0.5) if self.yScale[1]>0 else (self.yScale[1]*-0.5)
                        
                    elif self.choice == "Free":
                        if (max(self.parVals)-min(self.parVals))<=100:
                            
                            self.yScale = [int(ceil(min(self.parVals)-0.1*(max(self.parVals)-min(self.parVals)))),int(ceil(max(self.parVals)+0.1*(max(self.parVals)-min(self.parVals))))]
                            
         #                            self.yScale = [int(ceil(-2*max(self.parVals[self.par]))),int(ceil(2*max(self.parVals[self.par])))]
                        else:
                            self.yScale = [int(ceil(min(self.parVals)-0.1*(max(self.parVals)-min(self.parVals)))),int(ceil(max(self.parVals)+0.1*(max(self.parVals)-min(self.parVals))))]
                    
                    
                    self.ax.set_ylim(self.yScale[0],self.yScale[1])
                    
                
        
                    # for axes in self.figure.get_axes():
                    #     axes.set_xlabel("RADI (arcsec)")
                    #     axes.set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")
                    self.ax.set_xlabel("RADI (arcsec)")
                    self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                    
        
#                    self.ax.plot(self.parVals['RADI'], self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
                    self.ax.plot(self.parValRADI, self.parVals,'--bo')
         #           self.ax[i].set_title('Plot')
                    self.ax.set_xticks(self.parValRADI)
        
        
                    plt.tight_layout()
                    self.canvas.draw()
                    self.key = "No"  
                    break
#                else:
#                    print "false",counter
#                    counter += 1
        
  

class SMWindow(QtGui.QWidget):

    def __init__(self,par,xVal,gwDict):
        super(SMWindow, self).__init__()
        self.xMinVal = xVal[0]
        self.xMaxVal = xVal[1]
#        self.yMinVal = yVal[0]
#        self.yMaxVal = yVal[1]
        self.par = par
        self.gwDict = gwDict
        self.prevParVal = ""
        self.counter = 0
        
        self.parameter = QtGui.QComboBox()
#        self.parameter.setEditable(True)
        self.parameter.addItem("Select Parameter")
        for i in self.par:
            self.parameter.addItem(i)
        self.parameter.setAutoCompletion(True)
        self.parameter.setStyleSheet("QComboBox { combobox-popup: 0; }");
        self.parameter.setMaxVisibleItems(5)
        index = self.parameter.findText("Select Parameter",QtCore.Qt.MatchFixedString)
        self.parameter.setCurrentIndex(index)
        self.parameter.currentIndexChanged.connect(self.onChangeEvent)
        #run a for loop here to gather all they loaded parameters and populate as many text boxes
        
        self.xLabel = QtGui.QLabel("RADI")
        self.xMin = QtGui.QLineEdit()
        self.xMin.setPlaceholderText("RADI min ("+str(self.xMinVal)+")")
        self.xMax = QtGui.QLineEdit()
        self.xMax.setPlaceholderText("RADI max ("+str(self.xMaxVal)+")") 
        self.xGrid = QtGui.QGridLayout()
        self.xGrid.setSpacing(10)
        self.xGrid.addWidget(self.xLabel,1,0)
        self.xGrid.addWidget(self.xMin,2,0)
        self.xGrid.addWidget(self.xMax,2,1)
       
        self.yMin = QtGui.QLineEdit()
        self.yMax = QtGui.QLineEdit()
        self.yGrid = QtGui.QGridLayout()
        self.yGrid.setSpacing(10)
        self.yGrid.addWidget(self.parameter,1,0)
        self.yGrid.addWidget(self.yMin,2,0)
        self.yGrid.addWidget(self.yMax,2,1)
       
    
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addStretch(1)
        self.radioFree = QtGui.QRadioButton("Free")
        self.radioViewG = QtGui.QRadioButton("Beyond Viewgraph")
        self.hbox.addWidget(self.radioFree)
        self.hbox.addWidget(self.radioViewG)
        
        
        self.hboxBtns = QtGui.QHBoxLayout()
        self.hboxBtns.addStretch(1)
        self.btnUpdate = QtGui.QPushButton('Update', self)
       # self.btnUpdate.clicked.connect(self.updateScale)
        self.btnCancel = QtGui.QPushButton('Cancel', self)
        #self.btnCancel.clicked.connect(self.close)
        self.hboxBtns.addWidget(self.btnUpdate)
        self.hboxBtns.addWidget(self.btnCancel)
        
        self.fbox = QtGui.QFormLayout()
        self.fbox.addRow(self.xGrid)
        self.fbox.addRow(self.yGrid)
#        self.fbox.addRow(self.parameter)
#        self.fbox.addRow(self.yhbox)
        self.fbox.addRow(QtGui.QLabel("Scale Behaviour"),self.hbox)
        self.fbox.addRow(self.hboxBtns) 
    
        self.setLayout(self.fbox)
        self.setFocus()
        self.setWindowTitle("Scale Manager")
        self.setGeometry(300, 300, 300, 150)
        center(self)
        self.setFocus()

    def onChangeEvent(self):

        if not(len(self.yMin.text()) == 0):
            self.gwDict[self.prevParVal][0][0] = int(str(self.yMin.text()))
            self.gwDict[self.prevParVal][0][1] = int(str(self.yMax.text()))
            self.gwDict[self.prevParVal][1] = "Free" if self.radioFree.isChecked() else "Beyond Viewgraph"

            
        for i in self.par:
            if str(self.parameter.currentText()) == i:
                self.yMin.clear()
                self.yMin.setPlaceholderText(i+" min ("+str(self.gwDict[i][0][0])+")")
                self.yMax.clear()
                self.yMax.setPlaceholderText(i+" max ("+str(self.gwDict[i][0][1])+")")
                
                if str(self.gwDict[i][1]) == "Free":
                    self.radioFree.setChecked(True)
                    self.radioViewG.setChecked(False)
                else:
                    self.radioFree.setChecked(False)
                    self.radioViewG.setChecked(True)
                self.prevParVal = i

class ParamSpec(QtGui.QWidget):
    
    def __init__(self,par):
        super(ParamSpec, self).__init__()
        self.par = par
        
        self.parameterLabel = QtGui.QLabel("Parameter")
        self.parameter = QtGui.QComboBox()
        self.parameter.setEditable(True)
        self.parameter.addItem("Select Parameter")
        for i in self.par:
            self.parameter.addItem(i)
        self.parameter.setAutoCompletion(True)
        self.parameter.setStyleSheet("QComboBox { combobox-popup: 0; }");
        self.parameter.setMaxVisibleItems(6)
        index = self.parameter.findText("Select Parameter",QtCore.Qt.MatchFixedString)
        self.parameter.setCurrentIndex(index)
        
             
        self.uMeasLabel = QtGui.QLabel("Unit Measurement")        
        self.unitMeasurement = QtGui.QLineEdit()
#        self.unitMeasurement.setPlaceholderText("Unit Measurement")
      
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.parameterLabel, 1, 0)
        self.grid.addWidget(self.parameter, 1, 1)
        self.grid.addWidget(self.uMeasLabel, 2, 0)
        self.grid.addWidget(self.unitMeasurement, 2, 1)
       
        self.btnOK = QtGui.QPushButton('OK', self) 
        self.btnCancel = QtGui.QPushButton('Cancel', self)
        
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.btnOK)
        self.hbox.addWidget(self.btnCancel)
        
        self.grid.addLayout(self.hbox,3,1)
        self.setLayout(self.grid)
       
        self.setWindowTitle("Add Parameter")
        self.setGeometry(300, 300, 300, 150)

        center(self)
        self.setFocus()



class mainWindow(QtGui.QMainWindow): 
    key = "Yes"
    ncols = 1; nrows = 4
    currAx = "ax"; plotArea = "par"; ax = "someAxis"
    scaleChange = "No" ; scaleChangeR = 0
    choice = "Beyond Viewgraph"; choiceR = 0
    INSET = 'None'
    par = ['VROT','SBR','INCL','PA']; parR  = 0
    unitMeas = ['km/s','Jy km/s/sqarcs','degrees','degrees']; unitMeasR = 0
    tmpDeffile = os.getcwd() + "/tmpDeffile.def"
    
    gwObjects = []
    t = 0
    scrollWidth = 0; scrollHeight = 0
    
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
        super(mainWindow, self).__init__()
        self.initUI()
        
    
    def initUI(self):
        self.showMaximized()
        self.setWindowTitle('TiRiFiG') 
        
        self.cWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.cWidget)
        self.vLayout = QtGui.QVBoxLayout(self.cWidget)
                
        btn1 = QtGui.QPushButton('&Open File', self.cWidget) #you can ignore the parent and it will still work
        btn1.setFixedSize(80,30)
#        btn1.setFlat(True)
        btn1.setToolTip('Open .def file')
        btn1.clicked.connect(self.openDef)
        self.vLayout.addWidget(btn1)

        self.scrollArea = QtGui.QScrollArea(self.cWidget) # you can ignore the parent and it will still work
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContent = QtGui.QWidget(self.scrollArea)
        self.gridLayoutScroll = QtGui.QGridLayout(self.scrollAreaContent)
        self.scrollArea.setWidget(self.scrollAreaContent)
        
        self.vLayout.addWidget(self.scrollArea)
        
        
        
#        print self.width(), self.height()
        
        self.createActions()
        self.createMenus()  
        
       
    def createActions(self):
        self.exitAction = QtGui.QAction("&Exit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip('Leave the app')
        self.exitAction.triggered.connect(self.quitApp)

        self.openFile = QtGui.QAction("&Open File", self)
#        self.openFile.setShortcut("Ctrl+O")
        self.openFile.setStatusTip('Load .def file to be plotted')
        self.openFile.triggered.connect(self.openDef)
#        
        self.saveChanges = QtGui.QAction("&Save", self)
##        openEditor.setShortcut("Ctrl+S")
        self.saveChanges.setStatusTip('Save changes to .def file')
        self.saveChanges.triggered.connect(self.saveAll)
#        
        self.saveAsFile = QtGui.QAction("&Save as...",self)
        self.saveAsFile.setStatusTip('Create another .def file with current paramater values')
        self.saveAsFile.triggered.connect(self.saveAsAll)
#        
        self.openTextEditor = QtGui.QAction("&Open Text Editor...",self)
        self.openTextEditor.setStatusTip('View the current open .def file in preferred text editor')
        self.openTextEditor.triggered.connect(self.openEditor) # function yet to be written
#        
        self.startTF = QtGui.QAction("&Start TiriFiC",self)
        self.startTF.setStatusTip('Starts TiRiFiC from terminal')
        self.startTF.triggered.connect(self.startTiriFiC)
#
        self.winSpec = QtGui.QAction("&Window Specification",self)
        self.winSpec.setStatusTip('Determines the number of rows and columns in a plot')
        self.winSpec.triggered.connect(self.setRowCol)
#
        self.scaleMan = QtGui.QAction("&Scale Manager",self)
        self.scaleMan.setStatusTip('Manages behaviour of scale and min and max values')
        self.scaleMan.triggered.connect(self.SMobj)
#        
        self.paraDef = QtGui.QAction("&Parameter Definition",self)
        self.paraDef.setStatusTip('Determines which parameter is plotted')
        self.paraDef.triggered.connect(self.paraObj)
        
#        self.sm.radioFree.clicked.connect(self.getOptF)
#        self.sm.radioViewG.clicked.connect(self.getOptV)
#        self.sm.btnUpdate.clicked.connect(self.updateScale)
#        self.sm.btnCancel.clicked.connect(self.sm.close)

    def createMenus(self):
        mainMenu = self.menuBar()
        
        self.fileMenu = mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.openFile)
        self.fileMenu.addAction(self.saveChanges)
        self.fileMenu.addAction(self.saveAsFile)
        self.fileMenu.addAction(self.exitAction)
        
#        editMenu = mainMenu.addMenu('&Edit')
       
        self.runMenu = mainMenu.addMenu('&Run')
        self.runMenu.addAction(self.openTextEditor)
        self.runMenu.addAction(self.startTF)
        
        self.prefMenu = mainMenu.addMenu('&Preferences')
        self.prefMenu.addAction(self.scaleMan)
        self.prefMenu.addAction(self.paraDef)
        self.prefMenu.addAction(self.winSpec)
        
#    def reloadSM(self):
#        self.sm = SMWindow(self.gw.xScale[0],self.gw.xScale[1],self.gw.yScale[0],self.gw.yScale[1],self.gw.par)
#        self.sm.show()
#        self.sm.radioFree.clicked.connect(self.getOptF)
#        self.sm.radioViewG.clicked.connect(self.getOptV)
#        self.sm.btnUpdate.clicked.connect(self.updateScale)
#        self.sm.btnCancel.clicked.connect(self.sm.close)
#        self.ps.btnOK.clicked.connect(self.paramDef)
#        self.ps.btnCancel.clicked.connect(self.close)
#    
#    def getOptF(self):
#        self.gw.choice = "Free"
#
#    def getOptV(self):
#        self.gw.choice = "Beyond Viewgraph"

        
#        
    def quitApp(self):
        if self.t != 0:
            self.t.cancel()
        QtGui.qApp.quit()
        
        
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
            
        
    def openDef(self):
        """Opens data, gets parameters values, sets precision and sets scale
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Makes function calls to getData and getParameter functions, assigns values to dictionaries
        parVals andfirstPlot historyList and defines the x-scale and y-scale for plotting
        on viewgraph
        """  

        self.data = self.getData()
        
        if self.data == None:
            pass
        elif (not(self.data==None) or len(self.data)>0):
            self.getParameter(self.data)
            
#            see comment on keeping numPrecision as values in parVals dictionary
            
#            self.numPrecisionY = self.numPrecision(self.parVals['VROT'][:])
#            self.numPrecisionX = self.numPrecision(self.parVals['RADI'][:])

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
            if np.subtract(max(self.parVals['RADI']),min(self.parVals['RADI']))==0:
                self.xScale = [-100,100]
            elif np.subtract(max(self.parVals['RADI']),min(self.parVals['RADI']))<=100:
                self.xScale = [int(ceil(-2*max(self.parVals['RADI']))),int(ceil(2*max(self.parVals['RADI'])))]                           
            else:
                self.xScale = [int(ceil(min(self.parVals['RADI'])-0.1*(max(self.parVals['RADI'])-min(self.parVals['RADI'])))),int(ceil(max(self.parVals['RADI'])+0.1*(max(self.parVals['RADI'])-min(self.parVals['RADI']))))]                            
                
            for i in self.par:
                if np.subtract(max(self.parVals[i]),min(self.parVals[i]))==0:
                    self.yScale[i] = [-100,100]
                elif (max(self.parVals[i])-min(self.parVals[i]))<=100:
                    self.yScale[i] = [int(ceil(-2*max(self.parVals[i]))),int(ceil(2*max(self.parVals[i])))]
                else:
                    self.yScale[i] = [int(ceil(min(self.parVals[i])-0.1*(max(self.parVals[i])-min(self.parVals[i])))),int(ceil(max(self.parVals[i])+0.1*(max(self.parVals[i])-min(self.parVals[i]))))]
            
#            for i insetSizePolicy range(len(self.par)):
##                print "this is from mainWindow class"
##                print self.xScale,self.yScale[self.par[i]],self.choice,self.unitMeas[i],self.par[i],self.key
#                graph = GraphWidget(self.scrollArea,self.xScale,self.yScale[self.par[i]],self.choice,self.unitMeas[i],self.par[i],self.parVals,self.historyList,self.key,self.numPrecisionX,self.numPrecisionY)
#   
#                self.gridLayoutScroll.addWidget(graph)
#            
#            if self.ncols >=2:
#                width = self.widthMW/2
#                height = self.heightMW
#            else:
#                width = self.widthMW
#                height = self.heightMW
            print "MainWindow",self.width(),self.height()
            print "ScrollArea",self.scrollArea.width(),self.scrollArea.height()
            self.scrollWidth = self.scrollAreaContent.width(); self.scrollHeight = self.scrollAreaContent.height()
            counter = 0
            for i in range(self.nrows):
                for j in range(self.ncols):
                    self.gwObjects.append(GraphWidget(self.scrollArea,self.xScale,self.yScale[self.par[counter]],self.choice,self.unitMeas[counter],self.par[counter],self.parVals[self.par[counter]],self.parVals['RADI'],self.historyList[self.par[counter]],self.key,self.numPrecision(self.parVals['RADI'][:]),self.numPrecision(self.parVals[self.par[counter]][:])))
                    self.gwObjects[-1].btn1.clicked.connect(self.gwObjects[-1].changeGlobal)
                    self.gwObjects[-1].btn1.clicked.connect(self.paraObj)
                    self.gwObjects[-1].btn2.clicked.connect(self.gwObjects[-1].changeGlobal)
                    self.gwObjects[-1].btn2.clicked.connect(self.editParaObj)
                    self.gwObjects[-1].setMinimumSize(self.scrollWidth/2,self.scrollHeight/2)
                    self.gridLayoutScroll.addWidget(self.gwObjects[-1],i,j)
                    counter+=1
            
    def setRowCol(self):
         text,ok = QtGui.QInputDialog.getText(self,'Window number Input Dialog', 
                                            'Specify the number of rows and columns (5,5):')

         if ok:
            if len(text) > 0:

                text = str(text)
                text = text.split(",")

                self.nrows = int(text[0])
                self.ncols = int(text[1])
                if (self.nrows * self.ncols) >= len(self.par):
                    
#                    clear the existing graph objects before making new object for new grid
                    for i in reversed(range(self.gridLayoutScroll.count())):
                        self.gridLayoutScroll.itemAt(i).widget().setParent(None)
                        
                    counter = 0
                    for i in range(self.nrows):
                        for j in range(self.ncols):
                            self.gridLayoutScroll.addWidget(self.gwObjects[counter],i,j)
                            print self.gwObjects[-1].sizeHint()
                            counter+=1
                            if len(self.par) == counter:
                                break 
                else:
                    QtGui.QMessageBox.information(self, "Information", "Product of Rows and Columns should match the current number of parameters")

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
            
        #get the new values and format it as [0 20 30 40 50...]
        txt =""
        for i in range(len(newVals)):
            txt = txt+" " +'{0:.{1}f}'.format(newVals[i], self.numPrecisionY)

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
        for i in self.gwObjects:
            self.saveFile(i.parVals,i.par)
        
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
            
        #get the new values and format it as [0 20 30 40 50...]
        txt =""
        for i in range(len(newVals)):
            txt = txt+" " +'{0:.{1}f}'.format(newVals[i], self.numPrecisionY)

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
        for i in self.gwObjects:
            self.saveAs(fileName,i.parVals,i.par)
            
        self.saveAsMessage()
        
    
    def slotChangeData(self,fileName):

        with open(fileName) as f:
            self.data = f.readlines()
        f.close()
        

        self.getParameter(self.data)

        counter = 0
        for i in self.par:
            self.gwObjects[counter].parVals = self.parVals[i][:]
            self.gwObjects[counter].parValRADI = self.parVals['RADI'][:]
            
            counter+=1
#        ensure there are the same points for parameter as there are for RADI as specified in NUR parameter
#        diff = self.NUR-len(self.parVals[self.par])
#        lastItemIndex = len(self.parVals[self.par])-1
#        if diff == self.NUR:
#            for i in range(int(diff)):
#                self.parVals[self.par].append(0.0)
#        elif diff > 0 and diff < self.NUR:
#            for i in range(int(diff)):
#                self.parVals[self.par].append(self.parVals[self.par][lastItemIndex])
         #defining the x and y scale for plotting
        if (max(self.gwObjects[0].parValRADI)-min(self.gwObjects[0].parValRADI))<=100:
            xScale = [int(ceil(-2*max(self.gwObjects[0].parValRADI))),int(ceil(2*max(self.gwObjects[0].parValRADI)))]                           
        else:
            xScale = [int(ceil(min(self.gwObjects[0].parValRADI)-0.1*(max(self.gwObjects[0].parValRADI)-min(self.gwObjects[0].parValRADI)))),int(ceil(max(self.gwObjects[0].parValRADI)+0.1*(max(self.gwObjects[0].parValRADI)-min(self.gwObjects[0].parValRADI))))]                            
    
        for i in self.gwObjects:
#                self.saveFile(self.parVals[i],i)
#            print i.historyList[len(self.historyList)-1]
#            print i.parVals[:]
            if not(i.historyList[len(i.historyList)-1]==i.parVals[:]):
                i.historyList.append(i.parVals[:])
#        self.historyList.clear()
#        for i in self.parVals:
#            self.historyList[i] = [self.parVals[i][:]]
            
            i.xScale = xScale
            
            if (max(i.parVals)-min(i.parVals))<=100:
                i.yScale = [int(ceil(-2*max(i.parVals))),int(ceil(2*max(i.parVals)))]
            else:
                i.yScale = [int(ceil(min(i.parVals)-0.1*(max(i.parVals)-min(i.parVals)))),int(ceil(max(i.parVals)+0.1*(max(i.parVals)-min(i.parVals))))] 
            i.firstPlot()
#                
    def animate(self):
#        fileName = os.getcwd()
#        fileName += "/tmpDeffile.def"
        
        print "path is: ",self.tmpDeffile
        if os.path.isfile(self.tmpDeffile):
            
            after = os.stat(self.tmpDeffile).st_mtime
            if self.before != after:
                self.before = after
                print "changing data"
                self.slotChangeData(self.tmpDeffile)
            
#        
#        
    def openEditor(self):
        text,ok = QtGui.QInputDialog.getText(self,'Text Editor Input Dialog', 
                                            'Enter text editor:')
                                            
        if ok:
            
            for i in self.gwObjects:
                self.saveAs(self.tmpDeffile,i.parVals,i.par)

            if len(text)>0:
                programName = str(text)
                run([programName,self.tmpDeffile])
            else:
                run(["gedit",self.tmpDeffile])  
                
#            assign current modified time of temporary def file to before    
            self.before = os.stat(self.tmpDeffile).st_mtime
            
            self.t  = TimerThread(1,self.animate)
            self.t.start()

        
            
    def SMobj(self):
        filtGwObj = {}
        for i in self.gwObjects:
            filtGwObj[i.par] = [i.yScale,i.choice]
        self.sm = SMWindow(self.par,self.xScale,filtGwObj)
        self.sm.show()

        self.sm.btnUpdate.clicked.connect(self.updateScale)
        self.sm.btnCancel.clicked.connect(self.sm.close)
    
    def updateScale(self):
        
        if len(self.sm.xMin.text())>0:
            self.sm.xMinVal = int(str(self.sm.xMin.text()))
            self.sm.xMaxVal = int(str(self.sm.xMax.text()))
        
        print self.sm.prevParVal
        if len(self.sm.yMin.text())>0:
            self.sm.gwDict[self.sm.prevParVal][0][0] = int(str(self.sm.yMin.text()))
            self.sm.gwDict[self.sm.prevParVal][0][1] = int(str(self.sm.yMax.text()))
            self.sm.gwDict[self.sm.prevParVal][1] = "Free" if self.sm.radioFree.isChecked() else "Beyond Viewgraph"
#            print self.sm.gwDict[self.prevParVal][1]

        
        argKeys = [i for i in self.sm.gwDict]
        counter = 0
        for i in self.gwObjects:
            if i.par == argKeys[counter]:
                i.yScale = self.sm.gwDict[argKeys[counter]][0]
                i.choice = self.sm.gwDict[argKeys[counter]][1]
                i.xScale = [self.sm.xMinVal,self.sm.xMaxVal]  
                counter += 1
                """the first plot function should be invoked here"""
        print "about to print"
        self.sm.close
#        self.updateMessage()
        
        
    def updateMessage(self):
        """Displays the information about save action
        
        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the mainWindow class
        
        Returns:
        None
        
        Displays a messagebox that informs user that changes have been successfully written to the .def file
        """
        QtGui.QMessageBox.information(self, "Information", "Done!")
        
            
    def paraObj(self):
        
        val = []
        for i in self.parVals:
            if i in self.par:
                continue
            else:
                val.append(i)
                
        self.ps = ParamSpec(val)
        self.ps.show()
        self.ps.btnOK.clicked.connect(self.paramDef)
        self.ps.btnCancel.clicked.connect(self.ps.close)
            
    def paramDef(self):
        global currPar
        parIndex = self.par.index(currPar)
        
        if len(str(self.ps.parameter.currentText()))>0 and not(str.upper(str(self.ps.parameter.currentText())) in self.par):
            self.par.insert(parIndex+1,str.upper(str(self.ps.parameter.currentText())))
            self.unitMeas.insert(parIndex+1,str(self.ps.unitMeasurement.text()))
           
            if self.par[parIndex+1] in self.parVals:
                diff = self.NUR-len(self.parVals[self.par[parIndex+1]])
                if diff == self.NUR:
                    for i in range(diff):
                        self.parVals[self.par[parIndex+1]].append(0.0)
                elif diff > 0 and diff < self.NUR:
                    for i in range(diff):
                        self.parVals[self.par[parIndex+1]].append(self.parVals[self.par[parIndex+1]][-1])
                        
                if (len(self.historyList[self.par[parIndex+1]])==0) or ((len(self.historyList[self.par[parIndex+1]])>0) and not(self.historyList[self.par[parIndex+1]][-1]==self.parVals[self.par[parIndex+1]][:])):
                    self.historyList[self.par[parIndex+1]].append(self.parVals[self.par[parIndex+1]][:])
    
            else:
                zeroVals = []
                for i in range(self.NUR):
                    zeroVals.append(0.0)
                self.parVals[self.par[parIndex+1]] = zeroVals[:]
                del zeroVals
                self.historyList[self.par[parIndex+1]] = [self.parVals[self.par[parIndex+1]][:]]
               
            
            if max(self.parVals[self.par[parIndex+1]])<=0:
                self.yScale[self.par[parIndex+1]] = [-100,100]
            elif (max(self.parVals[self.par[parIndex+1]])-min(self.parVals[self.par[parIndex+1]]))<=100:
                self.yScale[self.par[parIndex+1]] = [int(ceil(-2*max(self.parVals[self.par[parIndex+1]]))),int(ceil(2*max(self.parVals[self.par[parIndex+1]])))]
            else:
                self.yScale[self.par[parIndex+1]] = [int(ceil(min(self.parVals[self.par[parIndex+1]])-0.1*(max(self.parVals[self.par[parIndex+1]])-min(self.parVals[self.par[parIndex+1]])))),int(ceil(max(self.parVals[self.par[parIndex+1]])+0.1*(max(self.parVals[self.par[parIndex+1]])-min(self.parVals[self.par[parIndex+1]]))))]
           
#            if self.par[-1] in [self.historyKeys[i][0] for i in range(len(self.historyKeys))]:
#               self.historyKeys.append([self.par,self.unitMeas,0])
#           else:
#               self.historyKeys.append([self.par,self.unitMeas,1])
#           self.historyKeysDup = collections.Counter([self.historyKeys[i][0] for i in range(len(self.historyKeys))])
#            self.key = "Yes"
            self.gwObjects.insert(parIndex+1,GraphWidget(self.scrollArea,self.xScale,self.yScale[self.par[parIndex+1]],self.choice,self.unitMeas[parIndex+1],self.par[parIndex+1],self.parVals[self.par[parIndex+1]],self.parVals['RADI'],self.historyList[self.par[parIndex+1]],self.key,self.numPrecision(self.parVals['RADI'][:]),self.numPrecision(self.parVals[self.par[parIndex+1]][:])))
            self.gwObjects[parIndex+1].setMinimumSize(self.scrollWidth/2,self.scrollHeight/2)
            self.nrows += 1
            for i in reversed(range(self.gridLayoutScroll.count())):
                self.gridLayoutScroll.itemAt(i).widget().setParent(None)
                
            counter = 0
            for i in range(self.nrows):
                for j in range(self.ncols):
#                    print "adding %d"%(counter+1)
                    self.gridLayoutScroll.addWidget(self.gwObjects[counter],i,j)
                    counter +=1
                    if len(self.par)-1 == counter:
                        break 
            
            self.gwObjects[parIndex+1].btn1.clicked.connect(self.gwObjects[parIndex+1].changeGlobal)
            self.gwObjects[parIndex+1].btn1.clicked.connect(self.paraObj)
            self.gwObjects[parIndex+1].btn2.clicked.connect(self.gwObjects[parIndex+1].changeGlobal)
            self.gwObjects[parIndex+1].btn2.clicked.connect(self.editParaObj)
                    
            self.ps.close()
            
    def editParaObj(self):
        val = []
        for i in self.parVals:
            if i in self.par:
                continue
            else:
                val.append(i)
                
        self.ps = ParamSpec(val)
        self.ps.show()
        self.ps.btnOK.clicked.connect(self.editParamDef)
        self.ps.btnCancel.clicked.connect(self.ps.close)
            
    def editParamDef(self):
        global currPar
        parIndex = self.par.index(currPar)
        if len(str(self.ps.parameter.currentText()))>0 and not(str.upper(str(self.ps.parameter.currentText())) in self.par):
            self.par[parIndex] = str.upper(str(self.ps.parameter.currentText()))
            self.unitMeas[parIndex] = str(self.ps.unitMeasurement.text())

           
            if self.par[parIndex] in self.parVals:
                diff = self.NUR-len(self.parVals[self.par[parIndex]])
                if diff == self.NUR:
                    for i in range(diff):
                        self.parVals[self.par[parIndex]].append(0.0)
                elif diff > 0 and diff < self.NUR:
                    for i in range(diff):
                        self.parVals[self.par[parIndex]].append(self.parVals[self.par[parIndex]][-1])
                        
                if (len(self.historyList[self.par[parIndex]])==0) or ((len(self.historyList[self.par[parIndex]])>0) and not(self.historyList[self.par[parIndex]][-1]==self.parVals[self.par[parIndex]][:])):
                    self.historyList[self.par[parIndex]].append(self.parVals[self.par[parIndex]][:])
    
            else:
                zeroVals = []
                for i in range(self.NUR):
                    zeroVals.append(0.0)
                self.parVals[self.par[parIndex]] = zeroVals[:]
                del zeroVals
                self.historyList[self.par[parIndex]] = [self.parVals[self.par[parIndex]][:]]
               
            
            if max(self.parVals[self.par[parIndex]])<=0:
                self.yScale[self.par[parIndex]] = [-100,100]
            elif (max(self.parVals[self.par[parIndex]])-min(self.parVals[self.par[parIndex]]))<=100:
                self.yScale[self.par[parIndex]] = [int(ceil(-2*max(self.parVals[self.par[parIndex]]))),int(ceil(2*max(self.parVals[self.par[parIndex]])))]
            else:
                self.yScale[self.par[parIndex]] = [int(ceil(min(self.parVals[self.par[parIndex]])-0.1*(max(self.parVals[self.par[parIndex]])-min(self.parVals[self.par[parIndex]])))),int(ceil(max(self.parVals[self.par[parIndex]])+0.1*(max(self.parVals[self.par[parIndex]])-min(self.parVals[self.par[parIndex]]))))]
           
#            if self.par[-1] in [self.historyKeys[i][0] for i in range(len(self.historyKeys))]:
#               self.historyKeys.append([self.par,self.unitMeas,0])
#           else:
#               self.historyKeys.append([self.par,self.unitMeas,1])
#           self.historyKeysDup = collections.Counter([self.historyKeys[i][0] for i in range(len(self.historyKeys))])
#            self.key = "Yes"
            for i in range(len(self.gwObjects)):
                if self.gwObjects[i].par == currPar:
                    self.gwObjects[i]=GraphWidget(self.scrollArea,self.xScale,self.yScale[self.par[parIndex]],self.choice,self.unitMeas[parIndex],self.par[parIndex],self.parVals[self.par[parIndex]],self.parVals['RADI'],self.historyList[self.par[parIndex]],self.key,self.numPrecision(self.parVals['RADI'][:]),self.numPrecision(self.parVals[self.par[parIndex]][:]))
                    self.gwObjects[i].setMinimumSize(self.scrollWidth/2,self.scrollHeight/2)

            for i in reversed(range(self.gridLayoutScroll.count())):
                self.gridLayoutScroll.itemAt(i).widget().setParent(None)
                
            counter = 0
            for i in range(self.nrows):
                for j in range(self.ncols):
                    print "adding %d"%(counter+1)
                    self.gridLayoutScroll.addWidget(self.gwObjects[counter],i,j)
                    counter +=1
                    if len(self.par)-1 == counter:
                        break 
            
            self.gwObjects[parIndex].btn1.clicked.connect(self.gwObjects[parIndex].changeGlobal)            
            self.gwObjects[parIndex].btn1.clicked.connect(self.paraObj)
            self.gwObjects[parIndex].btn2.clicked.connect(self.gwObjects[parIndex].changeGlobal)
            self.gwObjects[parIndex].btn2.clicked.connect(self.editParaObj)
            self.ps.close()

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
            for i in self.gwObjects:
                self.saveFile(i.parVals,i.par)
            os.system("gnome-terminal -e 'bash -c \"/home/samuel/software/TiRiFiC/tirific_2.3.4/bin/tirific deffile = "+self.fileName+"; exec bash\"'")
        else:
            self.tirificMessage()
           
def main():
    if os.path.isfile(os.getcwd() + "/tmpDeffile.def"):
        os.remove(os.getcwd() + "/tmpDeffile.def")

    app = QtGui.QApplication(sys.argv)
    GUI = mainWindow()
    GUI.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
