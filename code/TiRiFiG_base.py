# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:49:38 2017

@author: samuel

"""

#libraries
from PyQt4 import QtGui, QtCore
import os,sys
from subprocess import Popen as run
from math import ceil 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import style
style.use("ggplot")


#classes

class GraphWidget(QtGui.QWidget):
    
    key = "Yes"
    scaleChange = "No"
    choice = "Beyond Viewgraph"
    INSET = 'None'
    par = 'VROT'
    unitMeas = 'km/s'
    tmpDeffile = os.getcwd() + "/tmpDeffile.def"
    fileName = None
    
    before = 0
    numPrecisionY = 0
    numPrecisionX = 0
    NUR = 0
    data = []
    parVals = {}
    historyList = {}
    historyKeys= [['VROT','km/s']]
    xScale=[0,0]
    yScale=[0,0]
       
    
    mPress=[-5]
    mRelease=['None']
    mMotion=[-5]
    yVal = 0
    
    
    
    
    
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
                
            diff = self.NUR-len(self.parVals[self.par])
            lastItemIndex = len(self.parVals[self.par])-1
            if diff == self.NUR:
                for i in range(int(diff)):
                    self.parVals[self.par].append(0.0)
            elif diff > 0 and diff < self.NUR:
                for i in range(int(diff)):
                    self.parVals[self.par].append(self.parVals[self.par][lastItemIndex])
            
            self.historyList.clear()
            for i in self.parVals:
                self.historyList[i] = [self.parVals[i][:]]
            
            #defining the x and y scale for plotting

            if (max(self.parVals['RADI'])-min(self.parVals['RADI']))<=100:
                self.xScale = [int(ceil(-2*max(self.parVals['RADI']))),int(ceil(2*max(self.parVals['RADI'])))]                           
            else:
                self.xScale = [int(ceil(min(self.parVals['RADI'])-0.1*(max(self.parVals['RADI'])-min(self.parVals['RADI'])))),int(ceil(max(self.parVals['RADI'])+0.1*(max(self.parVals['RADI'])-min(self.parVals['RADI']))))]                            

            if (max(self.parVals['VROT'])-min(self.parVals['VROT']))<=100:
                self.yScale = [int(ceil(-2*max(self.parVals['VROT']))),int(ceil(2*max(self.parVals['VROT'])))]
            else:
                self.yScale = [int(ceil(min(self.parVals['VROT'])-0.1*(max(self.parVals['VROT'])-min(self.parVals['VROT'])))),int(ceil(max(self.parVals['VROT'])+0.1*(max(self.parVals['VROT'])-min(self.parVals['VROT']))))]
        
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
            self.mPress[0]=round(float(event.xdata),self.numPrecisionX)
            self.yVal = round(float(event.ydata),self.numPrecisionY)
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
        
        undoKey = event.key

        if str.lower(undoKey.encode('ascii','ignore')) == "ctrl+z":
            
            if (len(self.historyKeys)>1):
                
            #history list musn't be empty
        
                if len(self.historyList[self.historyKeys[-1][0]])>1:

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
                else:
                    self.historyKeys.pop()
                    self.par = self.historyKeys[-1][0]
                    self.unitMeas = self.historyKeys[-1][-1]

                    if (max(self.parVals[self.par])-min(self.parVals[self.par]))<=100:
                        self.yScale = [int(ceil(-2*max(self.parVals[self.par]))),int(ceil(2*max(self.parVals[self.par])))]
                    else:
                        self.yScale = [int(ceil(min(self.parVals[self.par])-0.1*(max(self.parVals[self.par])-min(self.parVals[self.par])))),int(ceil(max(self.parVals[self.par])+0.1*(max(self.parVals[self.par])-min(self.parVals[self.par]))))]
                    
                    self.key = "Yes"
                    self.plotFunc()
            else:
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
                        
                        if self.mMotion[0] >= 0.85*self.yScale[1]:
                            self.yScale[1] += (self.yScale[1]*0.1) if self.yScale[1]>0 else (self.yScale[1]*-0.1)
                            self.yScale[0] -= (self.yScale[0]*0.05) if self.yScale[0]>0 else (self.yScale[0]*-0.05)
                        elif self.mMotion[0] <= 0.85*self.yScale[0]:
                            self.yScale[0] -= (self.yScale[0]*0.1) if self.yScale[0]>0 else (self.yScale[0]*-0.1)
                            self.yScale[1] += (self.yScale[1]*0.05) if self.yScale[1]>0 else (self.yScale[1]*-0.05)
                        
                    elif self.choice == "Free":
                        if (max(self.parVals[self.par])-min(self.parVals[self.par]))<=100:
                            self.yScale = [int(ceil(-2*max(self.parVals[self.par]))),int(ceil(2*max(self.parVals[self.par])))]
                        else:
                            self.yScale = [int(ceil(min(self.parVals[self.par])-0.1*(max(self.parVals[self.par])-min(self.parVals[self.par])))),int(ceil(max(self.parVals[self.par])+0.1*(max(self.parVals[self.par])-min(self.parVals[self.par]))))]
                    

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
        
    def animate(self,i):
        fileName = os.getcwd()
        fileName += "/tmpDeffile.def"
        

        if os.path.isfile(self.tmpDeffile):
            
            after = os.stat(self.tmpDeffile).st_mtime
            if self.before != after:
                self.before = after
                self.slotChangeData(self.tmpDeffile)
        else:
            pass
        
        
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


class SMWindow(QtGui.QWidget):
    
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
 
           if self.gw.par in self.gw.historyList:
               if (len(self.gw.historyList[self.gw.par])<1) or ((len(self.gw.historyList[self.gw.par])>0) and not(self.gw.historyList[self.gw.par][-1]==self.gw.parVals[self.gw.par][:])):
                   self.gw.historyList[self.gw.par].append(self.gw.parVals[self.gw.par][:])
    
           else:
               self.gw.historyList[self.gw.par] = [self.gw.parVals[self.gw.par][:]]
            
            #print (historyList)
           if max(self.gw.parVals[self.gw.par])<=0:
               self.gw.yScale = [-100,100]
           elif (max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par]))<=100:
               self.gw.yScale = [int(ceil(-2*max(self.gw.parVals[self.gw.par]))),int(ceil(2*max(self.gw.parVals[self.gw.par])))]
           else:
               self.gw.yScale = [int(ceil(min(self.gw.parVals[self.gw.par])-0.1*(max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par])))),int(ceil(max(self.gw.parVals[self.gw.par])+0.1*(max(self.gw.parVals[self.gw.par])-min(self.gw.parVals[self.gw.par]))))]
           
           self.gw.historyKeys.append([self.gw.par,self.gw.unitMeas])
           self.gw.key = "Yes"
           self.gw.plotFunc()
           self.ps.close()

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = mainWindow()
        
    GUI.show()
    
    ani = animation.FuncAnimation(GUI.gw.figure, GUI.gw.animate, interval=100)

    app.exec_()


if __name__ == '__main__':
    main()

