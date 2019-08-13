usr/bin/env python
# -*- coding: UTF-8 -*-
#########################################################################################
# Author: Samuel (samueltwum1@gmail.com) with MSc supervisors                           #
# Copyright 2018 Samuel N. Twum                                                         #
#                                                                                       #
# GPL license - see LICENSE.txt for details                                             #
#########################################################################################

"""This script here is the GUI (PyQt4) implementation of TiRiFiG which allows users of
TiRiFiC to model tilted-ring parameters before fitting. Instructions on how TiRiFiC works
and everything you need to know about it can be found on the github pages:
http://gigjozsa.github.io/tirific/
As of now the code has been written in Python 2.7. Future considerations would be made to
have it run on Python 3 as well.

variables:
    currPar:  tilted-ring parameter whose graph widget window has focus

functions:
    main  : gets the whole thing started
    _center: centering application windows

classes:
    Timer:
        Class variables:  none

        Instance variables:
            t          (int):              the time(ms) when thread begins.
            hFunction  (function):         function to be executed by thread.
            thread     (function):         initialises and start the thread.

        Functions:
            __init__:                      initialises my instance variables.
            handle_function:               calls the function which the thread is run on.
            start:                         starts the thread.
            cancel:                        stops the thread.

    GraphWidget:
        Class variables:
            redo           (list):         the state of some parameters before undo
                                           action.
            mPress         (list):         x-y values of mouse click.
            mRelease       (list):         x-y values of mouse release.
            mMotion        (list):         x-y values of mouse motion.
            mDblPress      (list):         x-y values of mouse double click.

        Instance variables:
            xScale         (list):         upper and lower limit of x-axis.
            yScale         (list):         upper and lower limit of y-axis.
            unitMeas       (string):       the unit measurement for the parameter.
            par            (string):       a specific tilted-ring parameter.
            parVals        (list):         the values of  variable par (y-values on
                                           graph).
            parValRADI     (list):         the values of RADI (x-values on graph).
            historyList    (list):         the values of parVals for each time a point is
                                           shifted.
            key            (bool):         determines whether or not undo/redo key
                                           combination is pressed.
            numPrecisionX  (int):          the precision point to which a x-values are
                                           saved in.
            numPrecisionY  (int):          the precision point to which a y-values are
                                           saved in.
            canvas         (FigureCanvas): figure canvas where the subplots are made.
            btnAddParam    (QPushButton):  add a new plotted parameter to viewgraph.
            btnEditParam   (QPushButton):  change the parameter plotted to another
                                           parameter.

        Functions:
            __init__:                      initialises instance variables and starts
                                           graphWidget.
            changeGlobal:                  change the value of the global parameter
                                           (currPar) to reflect the parameter graphWidget
                                           is plotting.
            getClick:                      assigns x-y value captured from mouse
                                           left-click to mPress list or x-y value of.
                                           captured double click to mDblPress.
            getRelease:                    assigns x-y value captured from mouse release
                                           to mRelease list.
            getMotion:                     assigns x-y value captured from mouse motion
                                           to mMotion list.
            undoKey:                       sends the viewgraph back in history .
            redoKey:                       sends the viewgraph forward in history after
                                           an undo action.
            showInformation:               display information to say history list is
                                           exhausted when too many undo/redo actions are
                                           performed.
            firstPlot:                     produces plot of tilted-ring parameter(s) in
                                           viewgraph after .def file is opened.
            plotFunc:                      produces plot of tilted-ring parameter(s) in
                                           viewgraph when interacting with data points.

    SMWindow:
        Class Variables:  none

        Instance Variables:
            xMinVal        (int):          the value of the min x value of the parameter
                                           in focus.
            xMaxVal        (int):          the value of the max x value of the parameter
                                           in focus.
            par            (list):         list of all tilted-ring parameters
            gwDict         (dictionary):   filtered dictionary with only y-scale
            prevParVal     (string):       previous parameter value.
            parameter      (QComboBox):    drop down of all parameters retrieved from the
                                           variable <par>.
            xLabel         (QLabel):       label for RADI.
            xMin           (QLineEdit):    textbox for entering minimum value for RADI.
            xMax           (QLineEdit):    textbox for entering maximum value for RADI.
            yMin           (QLineEdit):    textbox for entering minimum value for
                                           selected parameter.
            yMax           (QLineEdit):    textbox for entering maximum value for
                                           selected parameter.
            btnUpdate      (QPushButton):  update variables with new values and close
                                           window.
            btnCancel      (QPushButton):  cancel changes and close window.

        Functions:
            __init__:                      initialises instance variables
            onChangeEvent:                 changes values of variables if the current
                                           index of the variable <parameter> changes.

    ParamSpec:
        Class Variables:  none

        Instance Variables:
            par             (list):        list of all tilted-ring parameters from .def
                                           file.
            parameterLabel  (QLabel):      label Parameter
            parameter       (QComboBox):   drop down of all tilted-ring parameters
                                           retrieved from the variable <par>.
            uMeasLabel      (QLabel):      label unit measurement
            unitMeasurement (QLineEdit):   textbox for entering unit measurement for
                                           parameter.
            btnOK           (QPushButton): updates the current parameter plotted to
                                           the new parameter specified.
            btnCancel       (QPushButton): close window

        Functions:
            __init__:                      initialises instance variables

    MainWindow:
        Class Variables:
            key             (string):      determines whether or not undo/redo key has
                                           been pressed.
            ncols           (int):         the number of columns in grid layout where
                                           viewgraphs are created.
            nrows           (int):         the number of rows in grid layout where
                                           viewgraphs are created.
            INSET           (string):      name of data cube retrieved from .def file.
            par             (list):        list of tilted-ring parameters which have
                                           their plots displayed in the viewgraph
            unitMeas        (list):        list of unit measurement for respective
                                           parameters in par list.
            tmpDeffile      (string):      path to temp file which is used to sync entry
                                           of data in text editor to viewgraph.
            gwObjects       (list):        list of graph widget objects each representing
                                           a tilted-ring parameter.
            t               (int):         thread which runs a separate process
                                           (open a text editor).
            scrollWidth     (int):         width of the scroll area.
            scrollHeight    (int):         height of the scroll area.
            before          (int):         time in milliseconds.
            numPrecisionY   (int):         precision in terms of number of decimal points
                                           to which values of parameter are handled.
            numPrecisionX   (int):         precision in terms of number of decimal points
                                           to which values of RADI are handled.
            NUR             (int):         number of rings as indicated in .def file.
            data            (list):        stream of text from .def file.
            parVals         (dictionary):  values of tilted-ring parameters.
            historyList     (dictionary):  values of tilted-ring parameters which have
                                           their values changed.
            xScale          (list):        upper and lower limit values of RADI axis
            yScale          (dictionary):  upper and lower limit values of parameter axis
            mPress          (list):        mouse x,y values when left mouse button is
                                           clicked.
            mRelease        (list):        mouse x,y values when the left mouse button
                                           is released.
            mMotion         (list):        mouse x,y values when mouse is moved.

        Instance Variables:
            cWidget        (QWidget):      central widget (main window).
            btnOpen        (QPushButton):  opens an open dialog box for user to choose
                                           the parameter file.
            scrollArea     (QScrollArea):  scroll area where graph widgets will be
                                           populated.
            mainMenu       (QMenu):        Menu bar with file menu, preference menu and
                                           run menu with each menu having different
                                           actions.

        Functions:
            __init__:                      creates the main window frame and calls the
                                           initUI function.
            initUI:                        initialises instance variables and creates
                                           menus with their actions.
            quitApp:                       closes TiRiFiG.
            cleaunUp:                      initialises class variables.
            getData:                       opens .def file and gets data from the file.
            strType:                       determines the data type of a variable.
            numPrecision:                  determines the floating point precision
                                           currently in .def file and sets it.
            getParameter:                  fetches the data points for the various
                                           tilted-ring parameters.
            openDef:                       calls getData and getParameter and creates the
                                           graph widgets for the default parameters
                                           (VROT, SBR, PA, INCL).
            undoCommand:                   undo last action for the current parameter in
                                           focus.
            redoCommand:                   redo last action for the current parameter in
                                           focus.
            setRowCol:                     specify the number of rows and columns in the
                                           grid layout.
            saveFile:                      save changes to file for one parameter.
            saveAll:                       calls saveFile function to save changes to
                                           file for all parameters.
            saveMessage:                   display information that save was successful.
            saveAs:                        save changes to a new file for one parameter.
            saveAsMessage:                 display information that save as was
                                           successful.
            saveAsAll:                     calls saveAs function to save changes for all
                                           parameters to a new file.
            slotChangeData:                change current viewgraph after making changes
                                           to .def file in text editor.
            animate:                       synchronise actions in text file to viewgraph
                                           with calls to slotChangeData function.
            openEditor:                    open preferred text editor.
            SMobj:                         instantiates the scale manager window and pops
                                           it.
            updateScale:                   updates the values in graph widget from what
                                           was entered in the scale manager window.
            updateMessage:                 displays information to say update was
                                           successful.
            add_parameter_dialog:          instantiates the parameter specfication class and
                                           connects btnOK to paramDef function for GW to be added
            insert_parameter_dialog:       instantiates the parameter specfication class and
                                           connects btnOK to paramDef function for GW to be inserted
            editParaObj:                   instantiates the parameter specfication class and
                                           connects btnOK to editParamDef function.
            paramDef:                      adds specified paramater viewgraph to layout.
            editParamDef:                  changes the parameter plotted in viewgraph to
                                           the specified parameter.
            tirificMessage:                displays information about input data cube not
                                           available in current working directory.
            startTiriFiC:                  starts TiRiFiC from terminal.
"""

# libraries
import os, sys, threading, time, logging
from subprocess import Popen as run
from math import ceil
from decimal import Decimal
import numpy as np
import matplotlib
matplotlib.use("qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import style
style.use("seaborn")
from PyQt5 import QtCore, QtWidgets

currPar = None
selected_option = None
fit_par = {'VROT':'km s-1',
           'SBR':'Jy km s-1 arcsec-2',
           'INCL':'degrees',
           'PA':'degrees',
           'RADI':'arcsec', 
           'Z0':'arcsec',
           'SDIS':'km s-1',
           'XPOS':'degrees',
           'YPOS':'degrees',
           'VSYS':'km s-1',
           'DVRO':'km s-1 arcsec-1',
           'DVRA':'km s-1 arcsec-1',
           'VRAD':'km s-1'}

def _center(self):
    """Centers the window

    Keyword arguments:
    self --         main window being displayed i.e. the current instance of the
                    mainWindow class

    Returns:
    None

    With information from the user's desktop, the screen resolution is  gotten
    and the center point is figured out for which the window is placed.
    """
    qr = self.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

class TimerThread():
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = threading.Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = threading.Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

class GraphWidget(QtWidgets.QWidget):
    redo = []
    mPress = [None, None]
    mRelease = [None, None]
    mMotion = [None]
    mDblPress = [None, None]
    last_value = 0

    def __init__(self, xScale, yScale, unitMeas, par, parVals, parValRADI,
                 historyList, key, numPrecisionX, numPrecisionY):
        super(GraphWidget, self).__init__()
        self.xScale = xScale
        self.yScale = yScale
        self.unitMeas = unitMeas
        self.par = par
        self.parVals = parVals
        self.parValRADI = parValRADI
        self.historyList = historyList
        self.key = key
        self.numPrecisionX = numPrecisionX
        self.numPrecisionY = numPrecisionY

        # Grid Layout
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        # Canvas and Toolbar
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)
        # self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        # self.canvas.setFocusPolicy( QtCore.Qt.WheelFocus )
        self.canvas.setFocus()


        self.canvas.mpl_connect('button_press_event', self.getClick)
        self.canvas.mpl_connect('button_release_event', self.getRelease)
        self.canvas.mpl_connect('motion_notify_event', self.getMotion)
        # self.canvas.mpl_connect('key_press_event', self.keyPressed)

        self.ax = self.figure.add_subplot(111)

        # button to add another tilted-ring parameter to plot
        self.btnAddParam = QtWidgets.QPushButton('&Add',self)
        self.btnAddParam.setFixedSize(50, 30)
        self.btnAddParam.setFlat(True)
        # FIX ME: use icon instead of text
        # self.btnAddParam.setIcon(QtGui.QIcon('utilities/icons/plus.png'))
        self.btnAddParam.setToolTip('Add Parameter')

        # modify plotted parameter
        self.btnEditParam = QtWidgets.QPushButton('&Change',self)
        self.btnEditParam.setFixedSize(80, 30)
        self.btnEditParam.setFlat(True)
        # FIX ME: use icon instead of text
        # self.btnEditParam.setIcon(QtGui.QIcon('utilities/icons/edit.png'))
        self.btnEditParam.setToolTip('Modify plotted parameter')

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.btnAddParam)
        hbox.addWidget(self.btnEditParam)

        grid.addLayout(hbox, 0, 0)
        grid.addWidget(self.canvas, 2, 0, 1, 2)

        self.firstPlot()

    def changeGlobal(self, val=None):
        global currPar
        if val == None:
            currPar = None
        else:
            currPar = self.par

    def _almost_equal(self, a, b, rel_tol=5e-2, abs_tol=0.0):
        '''Takes two values return true if they are almost equal'''
        diff = abs(b - a)
        return (diff <= abs(rel_tol * b)) or (diff <= abs_tol)
    
    def _over_and_above(self, a, b, switch):
        '''Takes two values return true if they are far apart'''
        # if input values are the same sign
        if (np.sign(a) == np.sign(b)):
            if switch == 'min':
                return a <= b
            else:
                return a >= b
        else:
            # case1: max +ve and top -ve
            # case2: min -ve and bottom +ve 
            return ((a > 0 and b < 0) or (a < 0 and b > 0))

    def getClick(self, event):
        """Left mouse button is clicked

        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the
                        mainWindow class
        event --        event type

        Returns:
        None

        The xData is captured when the left mouse button is clicked on the canvas
        """
        # on left click in figure canvas, captures mouse press and assign None to
        # mouse release


        if event.button == 1 and not event.xdata is None:
            self.mPress[0] = event.xdata
            self.mPress[1] = event.ydata
            self.mRelease[0] = None
            self.mRelease[1] = None

        if event.dblclick and not event.xdata is None:
            self.mDblPress[0] = event.xdata
            self.mDblPress[1] = event.ydata

            text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
                                                  'Enter new node value:')
            if ok:
                if text:
                    newVal = float(str(text))
                    for j in range(len(self.parValRADI)):
                        if ((self.mDblPress[0] < (self.parValRADI[j])+3) and
                            (self.mDblPress[0] > (self.parValRADI[j])-3)):

                            self.parVals[j] = newVal
                            bottom, top = self.ax.get_ylim()
                            self.ax.clear()
                            self.ax.set_xlim(self.xScale[0], self.xScale[1])
                            max_yvalue = max(self.parVals)
                            min_yvalue = min(self.parVals)

                            if self._over_and_above(min_yvalue, bottom, 'min'):
                                bottom = min_yvalue - (0.1*(max_yvalue-min_yvalue))
                                # this line is optional, only bottom scale should change
                                top = max_yvalue + (0.1*(max_yvalue-min_yvalue))
                            elif self._over_and_above(max_yvalue, top, 'max'):
                                top = max_yvalue + (0.1*(max_yvalue-min_yvalue))
                                # this line is optional, only top scale should change
                                bottom = min_yvalue - (0.1*(max_yvalue-min_yvalue))
                            elif self._almost_equal(min_yvalue, bottom, rel_tol=1e-2):
                                bottom = min_yvalue - (0.1*(max_yvalue-min_yvalue))
                                # this line is optional, only bottom scale should change
                                top = max_yvalue + (0.1*(max_yvalue-min_yvalue))
                            elif self._almost_equal(max_yvalue, top, rel_tol=1e-2):
                                top = max_yvalue + (0.1*(max_yvalue-min_yvalue))
                                # this line is optional, only top scale should change
                                bottom = min_yvalue - (0.1*(max_yvalue-min_yvalue))

                            self.ax.set_ylim(bottom, top)
                            self.ax.set_xlabel("RADI (arcsec)")
                            self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                            self.ax.plot(self.parValRADI, self.parVals, '--bo')
                            self.ax.set_xticks(self.parValRADI)
                            self.canvas.draw()
                            self.key = "No"
                            break

                    # append the new point to the history if the last item in history differs
                    # from the new point
                    if not self.historyList[len(self.historyList)-1] == self.parVals[:]:
                        self.historyList.append(self.parVals[:])

            self.mPress[0] = None
            self.mPress[1] = None

    def getRelease(self, event):
        """Left mouse button is released

        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the
                        mainWindow class
        event --        event type

        Returns:
        None

        The xData is captured when the left mouse button is released on the canvas.
        The new data point is added to the history and mouse pressed is assigned None
        """
        # re-look at this logic --seems to be a flaw somewhere


        if not event.ydata is None:
            self.mRelease[0] = event.xdata
            self.mRelease[1] = event.ydata
            self.changeGlobal()
            self.redo = []

        # append the new point to the history if the last item in history differs
        # from the new point
        if not self.historyList[len(self.historyList)-1] == self.parVals[:]:
            self.historyList.append(self.parVals[:])

        self.mPress[0] = None
        self.mPress[1] = None

    def getMotion(self, event):
        """Mouse is in motion

        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the
                        mainWindow class
        event --        event type

        Returns:
        None
        """
        # whilst the left mouse button is being clicked
        # capture the VROT (y-value) during mouse
        # movement and call re-draw graph

        if event.guiEvent.MouseMove == QtCore.QEvent.MouseMove:
            if event.button == QtCore.Qt.LeftButton:
                # if the mouse pointer moves out of the figure canvas use
                # the last value to redraw the graph
                if event.ydata is None:
                    self.last_value += 0.1 * self.last_value
                    self.mMotion[0] = self.last_value
                else:
                    self.last_value = event.ydata
                    self.mMotion[0] = event.ydata
                self.plotFunc()

    def undoKey(self):
        """Key is pressed

        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the
                        mainWindow class
        event --        event type

        Returns:
        None

        Deletes the last item in the history list when "Ctrl+z" is pressed and
        re-draws graph
        """
        if len(self.historyList) > 1:
            self.redo.append([self.numPrecisionY, self.parVals[:],
                              self.historyList[-1], self.yScale[:]])
            self.historyList.pop()
            self.parVals = self.historyList[-1][:]
            self.key = "Yes"
            self.plotFunc()
        else:
            self.showInformation()

    def redoKey(self):
        """Key is pressed

        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the
                        mainWindow class
        event --        event type

        Returns:
        None

        Deletes the last item in the history list when "Ctrl+z" is pressed and
        re-draws graph
        """

        if len(self.redo) > 0:
            self.numPrecisionY = self.redo[-1][2]
            self.parVals = self.redo[-1][3][:]
            self.historyList.append(self.redo[-1][4][:])
            self.yScale = self.redo[-1][5][:]
            self.redo.pop()
            self.key = "Yes"
            self.plotFunc()
        else:
            self.showInformation()


    def showInformation(self):
        """Show the information message

        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the
        mainWindow class

        Returns:
        None

        Displays a messagebox that informs user there's no previous action to be undone
        """
        QtWidgets.QMessageBox.information(self, "Information", "History list is exhausted")


    def firstPlot(self):
        """Plots data from file

        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the
        mainWindow class

        Returns:
        None

        Produces view graph from historyList
        """
        self.ax.clear()
        self.ax.set_xlim(self.xScale[0], self.xScale[1])
        self.ax.set_ylim(self.yScale[0], self.yScale[1])
        self.ax.set_xlabel("RADI (arcsec)")
        self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
        self.ax.plot(self.parValRADI, self.historyList[-1], '--bo')
        self.ax.set_xticks(self.parValRADI)
        self.canvas.draw()
        self.key = "No"

    def plotFunc(self):
        """Plots data from file

        Keyword arguments:
        self --         main window being displayed i.e. the current instance of the
                        mainWindow class

        Returns:
        None

        Produces view graph from historyList or parVals
        """

        if self.key == "Yes":
            self.firstPlot()

        # this re-plots the graph as long as the mouse is in motion and the right data
        # point is clicked
        else:
            for j in range(len(self.parValRADI)):
                if ((self.mPress[0] < (self.parValRADI[j]) + 3) and
                    (self.mPress[0] > (self.parValRADI[j]) - 3) and
                    (self.mRelease[0] is None)):
                    dy = self.mMotion[0] - self.parVals[j]
                    self.parVals[j]+=dy
                    bottom, top = self.ax.get_ylim()
                    self.ax.clear()
                    self.ax.set_xlim(self.xScale[0], self.xScale[1])
                    max_yvalue = max(self.parVals)
                    min_yvalue = min(self.parVals)

                    # FIX ME (sam 28/05/2019): scaling points too close to the limit should be relooked
                    # division by zero was encountered during runtime
                    if ((self.mMotion[0]/min_yvalue) >= 0.95) or ((self.mMotion[0]/max_yvalue) >= 0.95):
                        if self._almost_equal(self.mMotion[0], bottom, rel_tol=5e-2):
                            bottom = min_yvalue - (0.05*(max_yvalue-min_yvalue))
                            # this line is optional, only bottom scale should change
                            top = max_yvalue + (0.05*(max_yvalue-min_yvalue))
                        elif self._almost_equal(self.mMotion[0], top, rel_tol=5e-2):
                            top = max_yvalue + (0.05*(max_yvalue-min_yvalue))
                            # this line is optional, only top scale should change
                            bottom = min_yvalue - (0.05*(max_yvalue-min_yvalue))
                    else:
                        if self._almost_equal(self.mMotion[0], min_yvalue):
                            bottom = min_yvalue - (0.3*(max_yvalue-min_yvalue))
                            # this line is optional, only bottom scale should change
                            top = max_yvalue + (0.1*(max_yvalue-min_yvalue))
                        elif self._almost_equal(self.mMotion[0], max_yvalue):
                            top = max_yvalue + (0.3*(max_yvalue-min_yvalue))
                            # this line is optional, only top scale should change
                            bottom = min_yvalue - (0.1*(max_yvalue-min_yvalue))

                    self.ax.set_ylim(bottom, top)
                    self.ax.set_xlabel("RADI (arcsec)")
                    self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                    self.ax.plot(self.parValRADI, self.parVals, '--bo')
                    self.ax.set_xticks(self.parValRADI)
                    self.canvas.draw()
                    self.key = "No"
                    break

class SMWindow(QtWidgets.QWidget):

    def __init__(self, par, xVal, gwObjects):
        # TODO SAM (26/06/2019) no need to pass 'par' to init if we have 'gwObjects'
        # but maybe we need it because it makes things faster
        super(SMWindow, self).__init__()
        self.xMinVal = xVal[0]
        self.xMaxVal = xVal[1]
        self.gwObjects = gwObjects
        self.par = par
        self.prevParVal = ""
        self.counter = 0

        self.parameter = QtWidgets.QComboBox()
        # self.parameter.setEditable(True)
        self.parameter.addItem("Select Parameter")
        for i in self.par:
            self.parameter.addItem(i)
        # self.parameter.setAutoCompletion(True) : doesn't work in PyQt5
        self.parameter.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.parameter.setMaxVisibleItems(5)
        index = self.parameter.findText("Select Parameter", QtCore.Qt.MatchFixedString)
        self.parameter.setCurrentIndex(index)
        self.parameter.currentIndexChanged.connect(self.onChangeEvent)
        # run a for loop here to gather all they loaded parameters and populate as many text boxes

        self.xLabel = QtWidgets.QLabel("RADI")
        self.xMin = QtWidgets.QLineEdit()
        self.xMin.setPlaceholderText("RADI min ("+str(self.xMinVal)+")")
        self.xMax = QtWidgets.QLineEdit()
        self.xMax.setPlaceholderText("RADI max ("+str(self.xMaxVal)+")")
        self.xGrid = QtWidgets.QGridLayout()
        self.xGrid.setSpacing(10)
        self.xGrid.addWidget(self.xLabel, 1, 0)
        self.xGrid.addWidget(self.xMin, 2, 0)
        self.xGrid.addWidget(self.xMax, 2, 1)

        self.yMin = QtWidgets.QLineEdit()
        self.yMax = QtWidgets.QLineEdit()
        self.yGrid = QtWidgets.QGridLayout()
        self.yGrid.setSpacing(10)
        self.yGrid.addWidget(self.parameter, 1, 0)
        self.yGrid.addWidget(self.yMin, 2, 0)
        self.yGrid.addWidget(self.yMax, 2, 1)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addStretch(1)

        self.hboxBtns = QtWidgets.QHBoxLayout()
        self.hboxBtns.addStretch(1)
        self.btnUpdate = QtWidgets.QPushButton('Update', self)
        self.btnUpdate.clicked.connect(self.updateScale)
        self.btnCancel = QtWidgets.QPushButton('Cancel', self)
        self.btnCancel.clicked.connect(self.close)
        self.hboxBtns.addWidget(self.btnUpdate)
        self.hboxBtns.addWidget(self.btnCancel)

        self.fbox = QtWidgets.QFormLayout()
        self.fbox.addRow(self.xGrid)
        self.fbox.addRow(self.yGrid)
        self.fbox.addRow(self.hboxBtns)

        self.setLayout(self.fbox)
        self.setFocus()
        self.setWindowTitle("Scale Manager")
        self.setGeometry(300, 300, 300, 150)
        _center(self)
        self.setFocus()

        self.gwDict = {}
        for gwObject in self.gwObjects:
            self.gwDict[gwObject.par] = gwObject.yScale[:]

    def onChangeEvent(self):
        if self.yMin.text():
            self.gwDict[self.prevParVal][0] = int(str(self.yMin.text()))
        if self.yMax.text():
            self.gwDict[self.prevParVal][1] = int(str(self.yMax.text()))

        for i in self.par:
            if str(self.parameter.currentText()) == i:
                self.yMin.clear()
                self.yMin.setPlaceholderText(i+" min ("+str(self.gwDict[i][0])+")")
                self.yMax.clear()
                self.yMax.setPlaceholderText(i+" max ("+str(self.gwDict[i][1])+")")
                self.prevParVal = i

    def updateScale (self):
        """Change the values of the instance variables and specific graph widget plots
        after update button is clicked.
        """
        if self.xMin.text():
            self.xMinVal = int(str(self.xMin.text()))

        if self.xMax.text():
            self.xMaxVal = int(str(self.xMax.text()))

        if self.yMin.text():
            self.gwDict[self.prevParVal][0] = int(str(self.yMin.text()))

        if self.yMax.text():
            self.gwDict[self.prevParVal][1] = int(str(self.yMax.text()))

        for gwObject in self.gwObjects:
            gwObject.yScale = self.gwDict[gwObject.par][:]
            gwObject.xScale = [self.xMinVal, self.xMaxVal]
            gwObject.firstPlot()
        self.close()
        QtWidgets.QMessageBox.information(self, "Information", "Done!")


class ParamSpec(QtWidgets.QWidget):

    def __init__(self, par, windowTitle):
        super(ParamSpec, self).__init__()
        self.par = par

        self.parameterLabel = QtWidgets.QLabel("Parameter")
        self.parameter = QtWidgets.QComboBox()
        self.parameter.setEditable(True)
        self.parameter.addItem("Select Parameter")
        for i in self.par:
            self.parameter.addItem(i)

        self.parameter.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.parameter.setMaxVisibleItems(6)
        index = self.parameter.findText("Select Parameter", QtCore.Qt.MatchFixedString)
        self.parameter.setCurrentIndex(index)
        self.uMeasLabel = QtWidgets.QLabel("Unit Measurement")
        self.unitMeasurement = QtWidgets.QLineEdit()
        # self.unitMeasurement.setPlaceholderText("Unit Measurement")

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.parameterLabel, 1, 0)
        self.grid.addWidget(self.parameter, 1, 1)
        self.grid.addWidget(self.uMeasLabel, 2, 0)
        self.grid.addWidget(self.unitMeasurement, 2, 1)

        self.btnOK = QtWidgets.QPushButton('OK', self)
        self.btnCancel = QtWidgets.QPushButton('Cancel', self)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.btnOK)
        self.hbox.addWidget(self.btnCancel)

        self.grid.addLayout(self.hbox, 3, 1)
        self.setLayout(self.grid)

        self.setWindowTitle(windowTitle)
        self.setGeometry(300, 300, 300, 150)

        _center(self)
        self.setFocus()


class MainWindow(QtWidgets.QMainWindow):
    runNo = 0
    key = "Yes"
    loops = 0
    ncols = 1; nrows = 4
    INSET = 'None'
    par = ['VROT', 'SBR', 'INCL', 'PA']
    tmpDeffile = os.getcwd() + "/tmpDeffile.def"
    progressPath = ''
    fileName = ""
    gwObjects = []
    t = 0
    scrollWidth = 0; scrollHeight = 0
    before = 0
    numPrecisionY = {}
    numPrecisionX = 0
    NUR = 0
    data = []
    parVals = {}
    historyList = {}
    xScale = [0, 0]
    yScale = {'VROT':[0, 0]}
    mPress = [-5]
    mRelease = ['None']
    mMotion = [-5]

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()


    def initUI(self):
        self.showMaximized()
        self.setWindowTitle('TiRiFiG')
        # define a widget sitting in the main window where all other widgets will live
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        # make this new widget have a vertical layout
        vertical_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(vertical_layout)
        # add the buttons and the scroll area which will have the graph widgets
        # open button
        btnOpen = QtWidgets.QPushButton('&Open File')
        btnOpen.setFixedSize(80, 30)
        btnOpen.setToolTip('Open .def file')
        btnOpen.clicked.connect(self.openDef)
        vertical_layout.addWidget(btnOpen)
        # scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        # the scroll area needs a widget to be placed inside of it which will hold the content
        # create one and let it have a grid layout
        self.scroll_area_content = QtWidgets.QWidget()
        self.scroll_grid_layout = QtWidgets.QGridLayout()
        self.scroll_area_content.setLayout(self.scroll_grid_layout)
        scroll_area.setWidget(self.scroll_area_content)
        vertical_layout.addWidget(scroll_area)
        self.createActions()
        self.createMenus()

    def createActions(self):
        self.exitAction = QtWidgets.QAction("&Exit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip('Leave the app')
        self.exitAction.triggered.connect(self.quitApp)

        self.openFile = QtWidgets.QAction("&Open File", self)
        self.openFile.setShortcut("Ctrl+O")
        self.openFile.setStatusTip('Load .def file to be plotted')
        self.openFile.triggered.connect(self.openDef)

        self.saveChanges = QtWidgets.QAction("&Save", self)
        self.saveChanges.setStatusTip('Save changes to .def file')
        self.saveChanges.triggered.connect(self.saveAll)

        self.saveAsFile = QtWidgets.QAction("&Save as...", self)
        self.saveAsFile.setStatusTip('Create another .def file with current '
                                     'paramater values')
        self.saveAsFile.triggered.connect(self.saveAsAll)

        self.undoAction = QtWidgets.QAction("&Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.setStatusTip('Undo last action')
        self.undoAction.triggered.connect(self.undoCommand)

        self.redoAction = QtWidgets.QAction("&Redo", self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.setStatusTip('Redo last action')
        self.redoAction.triggered.connect(self.redoCommand)

        self.openTextEditor = QtWidgets.QAction("&Open Text Editor...", self)
        self.openTextEditor.setStatusTip('View the current open .def file in '
                                         'preferred text editor')
        self.openTextEditor.triggered.connect(self.openEditor)

        self.startTF = QtWidgets.QAction("&Start TiriFiC", self)
        self.startTF.setStatusTip('Starts TiRiFiC from terminal')
        self.startTF.triggered.connect(self.startTiriFiC)

        self.winSpec = QtWidgets.QAction("&Window Specification", self)
        self.winSpec.setStatusTip('Determines the number of rows and columns in a plot')
        self.winSpec.triggered.connect(self.setRowCol)

        self.scaleMan = QtWidgets.QAction("&Scale Manager", self)
        self.scaleMan.setStatusTip('Manages behaviour of scale and min and max values')
        self.scaleMan.triggered.connect(self.SMobj)

        self.paraDef = QtWidgets.QAction("&Parameter Definition", self)
        # self.paraDef.setStatusTip('Determines which parameter is plotted')
        self.paraDef.triggered.connect(self.add_parameter_dialog)

    def createMenus(self):
        mainMenu = self.menuBar()

        self.fileMenu = mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.openFile)
        self.fileMenu.addAction(self.undoAction)
        self.fileMenu.addAction(self.redoAction)
        self.fileMenu.addAction(self.saveChanges)
        self.fileMenu.addAction(self.saveAsFile)
        self.fileMenu.addAction(self.exitAction)

        # editMenu = mainMenu.addMenu('&Edit')

        self.runMenu = mainMenu.addMenu('&Run')
        self.runMenu.addAction(self.openTextEditor)
        self.runMenu.addAction(self.startTF)

        self.prefMenu = mainMenu.addMenu('&Preferences')
        self.prefMenu.addAction(self.scaleMan)
        self.prefMenu.addAction(self.paraDef)
        self.prefMenu.addAction(self.winSpec)

    def quitApp(self):
        if self.t != 0:
            self.t.cancel()
        QtWidgets.qApp.quit()

    def cleanUp(self):

        # FIXME(Samuel 11-06-2018): Find a way to do this better

        self.key = "Yes"
        self.ncols = 1; self.nrows = 4
        self.INSET = 'None'
        self.par = ['VROT', 'SBR', 'INCL', 'PA']
        self.unitMeas = ['km/s', 'Jy km/s/sqarcs', 'degrees', 'degrees']
        # FIXME use Lib/tempfile.py to create temporary file
        self.tmpDeffile = os.getcwd() + "/tmpDeffile.def"
        self.fileName = ""
        self.gwObjects = []
        self.t = 0
        self.scrollWidth = 0; self.scrollHeight = 0
        self.before = 0
        self.numPrecisionY = {}
        self.numPrecisionX = 0
        self.NUR = 0
        self.data = []
        self.parVals = {}
        self.historyList = {}
        self.xScale = [0, 0]
        self.yScale = {'VROT':[0, 0]}
        self.mPress = [-5]
        self.mRelease = ['None']
        self.mMotion = [-5]

        self.initUI()

    def getData(self):
        """Loads data from specified .def file in open dialog box

        Keyword arguments:
        self-- this is the main window being displayed
            i.e. the current instance of the mainWindow class

        Returns:
        data:list
        The text found in each line of the opened file

        data will be a none type variable if the fileName is invalid or no file is chosen
        """

        # stores file path of .def to fileName variable after user selects file in open
        # dialog box
        # TODO (Samuel 28-11-2018): If cancel is selected then suppress the message in try/except below
        self.fileName, _filter = QtWidgets.QFileDialog.getOpenFileName(self, "Open .def File", "~/",
                                                                       ".def Files (*.def)")

        # assign texts of read lines to data variable if fileName is exists, else assign
        # None
        try:
            with open(self.fileName) as f:
                data = f.readlines()
        except:
            if self.fileName == '':
                pass
            else:
                QtWidgets.QMessageBox.information(self, "Information",
                                                  "Empty/Invalid file specified")
            return None
        else:
            return data

    def strType(self, var):
        """Determines the data type of a variable

        Keyword arguments:
        self-- main window being displayed i.e. the current instance of the mainWindow class
        var-- variable holding the values

        Returns:
        int, float or str : string

        The function evaluates the data type of the var object and returns int,
        float or str
        """
        # why are you putting this in a try block (fixme)
        try:
            if int(var) == float(var):
                return 'int'
        except:
            try:
                float(var)
                return 'float'
            except:
                return 'str'

    def numPrecision(self, data):
        """Determines and sets floating point precision

        Keyword arguments:
        self-- main window being displayed i.e. the current instance of the mainWindow
               class
        data (list)--  list of scientific values of type string
                       e.g. x = ["20.00E4","55.0003E-4",...]

        Returns:
        int

        Determines the highest floating point precision of data points
        """

        decPoints = []
        # ensure values from list to are converted string
        # FIX ME: Consider using enumerate instead of iterating with range and len
        for i in range(len(data)):
            data[i] = str(data[i])

        for i in range(len(data)):
            val = data[i].split(".")
        # check val has decimal & fractional part and append length of numbers of
        # fractional part
            if len(val) == 2:
                decPoints.append(len(val[1].split('E')[0]))

        # assign greatest precision in decPoints to class variables handling precision
        if len(decPoints) == 0:
            return 0
        else:
            return max(decPoints)

    def getParameter(self, data):
        """Fetches data points of specified parameter

        Keyword arguments:
        self-- main window being displayed i.e. the current instance of the
               mainWindow class
        data (list)--  list containing texts of each line loaded from .def file

        Returns:
        parVal:list
        The values appearing after the '=' symbol of the parameter specified in sKey.
        If search key isnt found, zero values are returned

        The data points for the specific parameter value are located and converted
        from string to float data types for plotting and other data manipulation
        """
        # search through fetched data for values of "PAR =" or "PAR = " or "PAR=" or
        # "PAR= "
        global fit_par

        # I need NUR value first that's why it's on a different loop
        for i in data:
            lineVals = i.split("=")
            if len(lineVals) > 1:
                lineVals[0] = ''.join(lineVals[0].split())
                if lineVals[0].upper() == "NUR":
                    parVal = lineVals[1].split()
                    self.NUR = int(parVal[0])
                    break

        for i in data:
            lineVals = i.split("=")
            if len(lineVals) > 1:
                lineVals[0] = ''.join(lineVals[0].split())
                parVal = lineVals[1].split()

                if lineVals[0].upper() == "INSET":
                    self.INSET = ''.join(lineVals[1].split())
                elif lineVals[0].upper() == "LOOPS":
                    self.loops = int(parVal[0])
                else:
                    if (len(parVal) > 0 and not self.strType(parVal[0]) == 'str' and
                            not self.strType(parVal[-1]) == 'str' and
                            not self.strType(parVal[len(parVal) / 2]) == 'str'):
                        if (len(parVal) == self.NUR or lineVals[0].upper() in
                                fit_par.keys()):
                            if lineVals[0].upper() == 'RADI':
                                self.numPrecisionX = self.numPrecision(parVal[:])
                            else:
                                self.numPrecisionY[str.upper(lineVals[0])] = (
                                    self.numPrecision(parVal[:]))
                            for i in range(len(parVal)):
                                parVal[i] = float(Decimal(parVal[i]))
                            self.parVals[str.upper(lineVals[0])] = parVal[:]

    def openDef(self):
        """Opens data, gets parameter values, sets precision and sets scale

        Keyword arguments:
        self -- main window being displayed i.e. the current instance of the
                mainWindow class

        Returns:
        None

        Makes function calls to getData and getParameter functions, assigns
        values to dictionaries parVals and firstPlot historyList and defines
        the x-scale and y-scale for plotting on viewgraph
        """
        global fit_par
        data = self.getData()
        try:
            self.getParameter(data)
        except:
            if data is None:
                pass
            else:
                QtWidgets.QMessageBox.information(self, "Information",
                                                  "Tilted-ring parameters not retrieved")
                logging.info("The tilted-ring parameters could not be retrieved from the {}"
                             .format(self.fileName))
        else:
            self.data = data
            if self.runNo > 0:
                # FIXME reloading another file on already opened not properly working
                # user has to close open window and reopen file for such a case
                QtWidgets.QMessageBox.information(self, "Information",
                                                  "Close app and reopen to load file. Bug "
                                                  "being fixed")
                # self.cleanUp()
                # FIXME (Samuel 11-06-2018): Find a better way to do this
                # self.data = data
                # self.getParameter(self.data)
            else:
                # defining the x scale for plotting
                # this is the min/max + 10% of the difference between the min and max
                min_max_diff = max(self.parVals['RADI']) - min(self.parVals['RADI'])
                percentage_of_min_max_diff = 0.1 * min_max_diff
                lower_bound = min(self.parVals['RADI']) - percentage_of_min_max_diff
                upper_bound = max(self.parVals['RADI']) + percentage_of_min_max_diff
                self.xScale = [int(ceil(lower_bound)), int(ceil(upper_bound))]
                
                self.scrollWidth = self.scroll_area_content.width()
                self.scrollHeight = self.scroll_area_content.height()

                # make a dict to save the graph widgets to be plotted
                # note that this approach will require another loop.
                # Not ideal but it gets the job done for now.
                g_w_to_plot = {}
                # ensure there are the same points for parameters as there are for RADI as
                # specified in NUR parameter
                for key, val in self.parVals.items():
                    diff = self.NUR - len(val)
                    if key == 'RADI': #use this implementation in other diff checkers
                        if diff == self.NUR:
                            for j in np.arange(0.0, (int(diff) * 40.0), 40):
                                self.parVals[key].append(j)
                        elif diff > 0 and diff < self.NUR:
                            for j in range(int(diff)):
                                self.parVals[key].append(self.parVals[key][-1] + 40.0)
                        continue
                    else:
                        if diff == self.NUR:
                            for j in range(int(diff)):
                                self.parVals[key].append(0.0)
                        elif diff > 0 and diff < self.NUR:
                            for j in range(int(diff)):
                                self.parVals[key].append(val[-1])

                    self.historyList.clear()
                    self.historyList[key] = [self.parVals[key][:]]

                    min_max_diff = max(self.parVals[key]) - min(self.parVals[key])
                    percentage_of_min_max_diff = 0.1 * min_max_diff
                    lower_bound = min(self.parVals[key]) - percentage_of_min_max_diff
                    upper_bound = max(self.parVals[key]) + percentage_of_min_max_diff
                    # are the min/max values the same
                    if np.subtract(max(self.parVals[key]), min(self.parVals[key])) == 0:
                        self.yScale[key] = [lower_bound/2, upper_bound*1.5]
                    else:
                        self.yScale[key] = [lower_bound, upper_bound]
                    
                    unit = fit_par[key] if key in fit_par.keys() else ""
                    self.gwObjects.append(GraphWidget(self.xScale,
                                                      self.yScale[key][:],
                                                      unit, key,
                                                      self.parVals[key][:],
                                                      self.parVals['RADI'][:],
                                                      self.historyList[key][:],
                                                      self.key, self.numPrecisionX,
                                                      self.numPrecisionY[key]))
                    self.gwObjects[-1].btnAddParam.clicked.connect(
                        self.gwObjects[-1].changeGlobal)
                    self.gwObjects[-1].btnAddParam.clicked.connect(
                        self.insert_parameter_dialog)
                    self.gwObjects[-1].btnEditParam.clicked.connect(
                        self.gwObjects[-1].changeGlobal)
                    self.gwObjects[-1].btnEditParam.clicked.connect(
                        self.editParaObj)
                    # TODO we should also probably set the minimum size for the scroll layout
                    self.gwObjects[-1].setMinimumSize(self.scrollWidth/2, self.scrollHeight/2)
                    if key in self.par:
                        g_w_to_plot[key] = self.gwObjects[-1]

                # retrieve the values in order and build a list of ordered key-value pairs
                ordered_dict_items = [(key, g_w_to_plot[key]) for key in self.par]
                for idx, items in enumerate(ordered_dict_items):
                    graph_widget = items[1] # what does 1 represent
                    self.scroll_grid_layout.addWidget(graph_widget, idx, 0)
                del g_w_to_plot, ordered_dict_items
                self.runNo+=1

    def undoCommand(self):
        global currPar
        for i in range(len(self.gwObjects)):
            if self.gwObjects[i].par == currPar:
                self.gwObjects[i].undoKey()
                break

    def redoCommand(self):
        global currPar
        for i in range(len(self.gwObjects)):
            if self.gwObjects[i].par == currPar:
                self.gwObjects[i].redoKey()
                break

    def setRowCol(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Window number Input Dialog",
                                                  "Specify the number of rows and columns (5,5):")
        if ok:
            if text:
                text = str(text)
                text = text.split(",")
                self.nrows = int(text[0])
                self.ncols = int(text[1])
                if (self.nrows * self.ncols) >= len(self.par):
                    # clear the existing graph objects
                    item_count = self.scroll_grid_layout.count()
                    for i in range(item_count):
                        widget_to_remove = self.scroll_grid_layout.itemAt(0).widget()
                        self.scroll_grid_layout.removeWidget(widget_to_remove)
                        widget_to_remove.close()

                    # get only the plot widgets for the we want to plot: defined in par
                    g_w_to_plot = [gwObject for gwObject in self.gwObjects
                                   if gwObject.par in self.par]
                    # retrieve the parameter for each graph widget in the g_w_to_plot list
                    # self.par for instance contains [VROT, SBR, PA and INCL]
                    # g_w_pars will also contain a list of parameters but in the order
                    # of self.gwObjects e.g. new_par = [PA, SBR, VROT, INCL].
                    # Create a new sorted list of graph widgets based as below:
                    # loop through self.par [VROT, SBR, PA, INCL]grab the index of the 
                    # parameter in the new_par list [PA, SBR, VROT, INCL] i.e. 
                    # index(VROT) in new_par list: 2
                    # index(SBR) in new_par list: 1
                    # index(PA) in new_par list: 0
                    # index(INCL) in new_par list: 3
                    # Use these indexes to get a sorted list of graph widgets
                    # from g_w_to_plot for the plotting
                    g_w_pars = [g_w.par for g_w in g_w_to_plot]
                    sorted_g_w_to_plot = []
                    for par in self.par:
                        idx = g_w_pars.index(par)
                        sorted_g_w_to_plot.append(g_w_to_plot[idx])
                    # delete the unordered list of graph widgets
                    del g_w_to_plot

                    counter = 0
                    for i in range(self.nrows):
                        for j in range(self.ncols):
                            self.scroll_grid_layout.addWidget(
                                sorted_g_w_to_plot[counter], i, j)
                            # call the show method on the graphWidget object in order to
                            # display it
                            sorted_g_w_to_plot[counter].show()
                            # don't bother iterating to plot if all the parameters have been
                            # plotted else you'll get an error
                            if counter == len(sorted_g_w_to_plot) -1 :
                                break
                            counter += 1
                    del sorted_g_w_to_plot
                else:
                    QtWidgets.QMessageBox.information(self, "Information",
                                                      "Product of rows and columns should"
                                                      " match the current number of parameters"
                                                      " on viewgraph")

    def saveFile(self, newVals, sKey, unitMeasurement, numPrecisionX, numPrecisionY):
        """Save changes made to data points to .def file per specified parameter

        Keyword arguments:
        self--  main window being displayed i.e. the current instance of the
        mainWindow class
        newVals (list)-- list containing new values
        sKey (str)-- parameter search key

        Returns:
        None

        The .def file would be re-opened and updated per the new values that
        are contained in the parVal* variable
        """

        # get the new values and format it as e.g. [0 20 30 40 50...]
        txt = ""
        for i in range(len(newVals)):
            if sKey == 'RADI':
                txt = txt+" " +'{0:.{1}E}'.format(newVals[i], numPrecisionX)
            else:
                txt = txt+" " +'{0:.{1}E}'.format(newVals[i], numPrecisionY)

        # FIXME (11-06-2018) put this block of code in a try except block
        tmpFile = []
        with open(self.fileName, 'a') as f:
            status = False
            for i in self.data:
                lineVals = i.split("=")
                if len(lineVals) > 1:
                    lineVals[0] = ''.join(lineVals[0].split())
                    if sKey == lineVals[0]:
                        txt = "    "+sKey+"="+txt+"\n"
                        tmpFile.append(txt)
                        status = True
                    else:
                        tmpFile.append(i)
                else:
                    tmpFile.append(i)

            if not status:
                tmpFile.append("# "+sKey+" parameter in "+unitMeasurement+"\n")
                txt = "    "+sKey+"="+txt+"\n"
                tmpFile.append(txt)

            f.seek(0)
            f.truncate()
            for i in tmpFile:
                f.write(i)

            self.data = tmpFile[:]

    def saveAll(self):
        """Save changes made to data point to .def file for all parameters

        Keyword arguments:
        self -- main window being displayed i.e. the current instance of
        the mainWindow class

        Returns:
        None

        The saveFile function is called and updated with the current values being
        held by parameters.
        """
        for i in self.gwObjects:
            self.saveFile(i.parVals, i.par, i.unitMeas, i.numPrecisionX, i.numPrecisionY)

        self.saveMessage()

    def saveMessage(self):
        """Displays the information about save action

        Keyword arguments:
        self--  main window being displayed i.e. the current instance of the mainWindow class

        Returns:
        None

        Displays a messagebox that informs user that changes have been successfully
        written to the .def file
        """
        QtWidgets.QMessageBox.information(self, "Information",
                                          "Changes successfully written to file")

    def saveAs(self, fileName, newVals, sKey, unitMeasurement, numPrecisionX,
               numPrecisionY):
        """Creates a new .def file with current data points on viewgraph

        Keyword arguments:
        self--  main window being displayed i.e. the current instance of the
                mainWindow class
        fileName--  filePath where new file should be saved to
        newVals (list)--    list containing new values
        sKey (str)--    parameter search key

        Returns:
        None

        A new .def file would be created and placed in the specified file path
        """

        # get the new values and format it as [0 20 30 40 50...]
        txt = ""
        for i in range(len(newVals)):
            if sKey == 'RADI':
                txt = txt+" " +'{0:.{1}E}'.format(newVals[i], numPrecisionX)
            else:
                txt = txt+" " +'{0:.{1}E}'.format(newVals[i], numPrecisionY)

        tmpFile = []

        if not fileName == None:
            with open(fileName, 'a') as f:
                status = False
                for i in self.data:
                    lineVals = i.split("=")
                    if len(lineVals) > 1:
                        lineVals[0] = ''.join(lineVals[0].split())
                        if sKey == lineVals[0]:
                            txt = "    "+sKey+"="+txt+"\n"
                            tmpFile.append(txt)
                            status = True
                        else:
                            tmpFile.append(i)
                    else:
                        tmpFile.append(i)

                if not status:
                    tmpFile.append("# "+sKey+" parameter in "+unitMeasurement+"\n")
                    txt = "    "+sKey+"="+txt+"\n"
                    tmpFile.append(txt)

                f.seek(0)
                f.truncate()
                for i in tmpFile:
                    f.write(i)

                self.data = tmpFile[:]
                self.fileName = fileName

    def saveAsMessage(self):
        """Displays the information about save action

        Keyword arguments:
        self--  main window being displayed i.e. the current instance of the
                mainWindow class

        Returns:
        None

        Displays a messagebox that informs user that changes have been successfully
        written to the .def file
        """
        QtWidgets.QMessageBox.information(self, "Information", "File Successfully Saved")

    def saveAsAll(self):
        """Creates a new .def file for all parameters in current .def file opened

        Keyword arguments:
        self--  main window being displayed i.e. the current instance of
        the mainWindow class

        Returns:
        None

        The saveAs function is called and updated with the current values being
        held by parameters.
        """
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, "Save .def file as ",
                                                         os.getcwd(),
                                                         ".def Files (*.def)")
        for i in self.gwObjects:
            self.saveAs(fileName, i.parVals, i.par, i.unitMeas, i.numPrecisionX,
                        i.numPrecisionY)

        self.saveAsMessage()

    def slotChangeData(self, fileName):
        global fit_par
        with open(fileName) as f:
            self.data = f.readlines()

        self.getParameter(self.data)

        # counter = 0
        for i in fit_par.keys():
            for j in self.gwObjects:
                if j.par == i:
                    j.parVals = self.parVals[i][:]
                    j.parValRADI = self.parVals['RADI'][:]

        # FIXME(Samuel 11-06-2018):
        # the comments below will probably be important to keep/implement
        # it's possible that the user will delete some points in the .def file

        # ensure there are the same points for parameter as there are for RADI as
        # specified in NUR parameter
        # diff = self.NUR-len(self.parVals[self.par])
        # lastItemIndex = len(self.parVals[self.par])-1
        # if diff == self.NUR:
        #    for i in range(int(diff)):
        #        self.parVals[self.par].append(0.0)
        # elif diff > 0 and diff < self.NUR:
        #    for i in range(int(diff)):
        #        self.parVals[self.par].append(self.parVals[self.par][lastItemIndex])

        # defining the x and y scale for plotting
        if (np.subtract(max(self.gwObjects[0].parValRADI),
                        min(self.gwObjects[0].parValRADI)) == 0):
            self.xScale = [-100, 100]
        elif ((max(self.gwObjects[0].parValRADI) -
               min(self.gwObjects[0].parValRADI)) <= 100):
            self.xScale = [int(ceil(-2 * max(self.gwObjects[0].parValRADI))),
                           int(ceil(2 * max(self.gwObjects[0].parValRADI)))]
        else:
            self.xScale = [int(ceil(min(self.gwObjects[0].parValRADI) -
                                    0.1 * (max(self.gwObjects[0].parValRADI) -
                                           min(self.gwObjects[0].parValRADI)))),
                           int(ceil(max(self.gwObjects[0].parValRADI) +
                                    0.1 * (max(self.gwObjects[0].parValRADI) -
                                           min(self.gwObjects[0].parValRADI))))]

        for i in self.gwObjects:
            if not i.historyList[len(i.historyList)-1] == i.parVals[:]:
                i.historyList.append(i.parVals[:])

            i.xScale = self.xScale
            if np.subtract(max(i.parVals), min(i.parVals)) == 0:
                i.yScale = [-100, 100]
            elif (max(i.parVals)-min(i.parVals)) <= 100:
                i.yScale = [int(ceil(-2 * max(i.parVals))),
                            int(ceil(2 * max(i.parVals)))]
            else:
                i.yScale = [int(ceil(min(i.parVals) -
                                     0.1 * (max(i.parVals) - min(i.parVals)))),
                            int(ceil(max(i.parVals) + 0.1 * (max(i.parVals) -
                                                             min(i.parVals))))]
            i.firstPlot()

    def animate(self):
        if os.path.isfile(self.tmpDeffile):
            after = os.stat(self.tmpDeffile).st_mtime
            if self.before != after:
                self.before = after
                self.slotChangeData(self.tmpDeffile)

    def openEditor(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Text Editor Input Dialog",
                                                  "Enter text editor:")
        if ok:

            for i in self.gwObjects:
                self.saveAs(self.tmpDeffile, i.parVals, i.par, i.unitMeas,
                            i.numPrecisionX, i.numPrecisionY)

            if text:
                programName = str(text)
                try:
                    run([programName, self.tmpDeffile])
                except OSError:
                    QtWidgets.QMessageBox.information(self, "Information",
                                                      "{} is not installed or configured"
                                                      "properly on this system.".format(programName))
            else:
                # assign current modified time of temporary def file to before
                self.before = os.stat(self.tmpDeffile).st_mtime
                self.t = TimerThread(1, self.animate)
                self.t.start()

    def inProgress(self):
        """Displays the information about feature under development
        """
        QtWidgets.QMessageBox.information(self, "Information",
                                          "This feature is under development")

    def SMobj(self):
        self.sm = SMWindow(self.par, self.xScale, self.gwObjects)
        self.sm.show()

    def paramDef(self):
        global currPar, fit_par, selected_option
        user_input = self.ps.parameter.currentText()
        # check if the inputted parameter value has its plot displayed
        if (user_input and
            not str.upper(str(user_input)) in self.par):
            # the graph for the new tilted ring parameter will be inserted right after
            # the tilted ring parameter which has focus (defined in currPar)
            # if no tilted ring parameter has focus then the graph of the new tilted ring
            # parameter will be placed in the last position
            if currPar:
                if selected_option == 'insert':
                    parIndex = self.par.index(currPar)
                    parIndex += 1
                else:
                    raise ValueError ("Expecting an insert option but got {}".
                                      format(selected_option))
            else:
                if selected_option == 'add':
                    parIndex = len(self.par)
                else:
                    raise ValueError("Expecting an add option but got {}".
                                     format(selected_option))
            self.par.insert(parIndex,
                            str.upper(str(user_input)))

            unitMeas = str(self.ps.unitMeasurement.text())

            # only parameters in the self.par variable have their plots displayed.
            # other parameters specified in the .def file each have a graph widget
            # object saved as part of the gwObjects list. Handle cases where new parameter
            # to be plotted doesn't exist in the expected tilted ring parameters (defined
            # as fit_par) or wasn't defined in the .def file.
            tilted_ring_par = self.par[parIndex]
            if tilted_ring_par not in fit_par.keys():
                fit_par[tilted_ring_par] = unitMeas
            # check if new tilted ring parameter isn't already in the list of gwObjects
            list_of_t_r_p = [gwObject.par for gwObject in self.gwObjects]
            if tilted_ring_par not in list_of_t_r_p:
                zeroVals = [0.0] * self.NUR
                self.parVals[tilted_ring_par] = zeroVals[:]
                del zeroVals
                self.historyList[tilted_ring_par] = (
                    [self.parVals[tilted_ring_par][:]])
                self.yScale[tilted_ring_par] = [-100, 100]
                fit_par[tilted_ring_par] = unitMeas
                self.gwObjects.insert(parIndex,
                                      GraphWidget(self.xScale,
                                                  self.yScale[tilted_ring_par],
                                                  unitMeas,
                                                  tilted_ring_par,
                                                  self.parVals[tilted_ring_par],
                                                  self.parVals['RADI'],
                                                  self.historyList[tilted_ring_par],
                                                  "Yes",
                                                  self.numPrecisionX,
                                                  1))
                self.gwObjects[parIndex].setMinimumSize(self.scrollWidth/2,
                                                        self.scrollHeight/2)
                self.gwObjects[parIndex].btnAddParam.clicked.connect(
                    self.gwObjects[parIndex].changeGlobal)
                self.gwObjects[parIndex].btnAddParam.clicked.connect(
                    self.insert_parameter_dialog)
                self.gwObjects[parIndex].btnEditParam.clicked.connect(
                    self.gwObjects[parIndex].changeGlobal)
                self.gwObjects[parIndex].btnEditParam.clicked.connect(
                    self.editParaObj)
                del list_of_t_r_p

            self.nrows = self.scroll_grid_layout.rowCount()
            self.ncols = self.scroll_grid_layout.columnCount()
            item_count = self.scroll_grid_layout.count()
            if selected_option == "add":
                g_w_to_plot = [gwObject for gwObject in self.gwObjects
                               if gwObject.par == tilted_ring_par][0]
                last_item_index = item_count - 1
                graph_widget_position = (
                    self.scroll_grid_layout.getItemPosition(last_item_index))
                row_number = graph_widget_position[0]
                column_number = graph_widget_position[1]
                if column_number < self.ncols:
                    self.scroll_grid_layout.addWidget(
                        g_w_to_plot, row_number, column_number + 1)
                else:
                    if row_number == self.nrows:
                        self.nrows += 1 # does this even matter
                    self.scroll_grid_layout.addWidget(g_w_to_plot, row_number + 1, 0)

                del g_w_to_plot
            else:
                self.nrows += 1

                for i in range(item_count):
                    widget_to_remove = self.scroll_grid_layout.itemAt(0).widget()
                    self.scroll_grid_layout.removeWidget(widget_to_remove)
                    widget_to_remove.close()

                # get only the plot widgets for the we want to plot: defined in par
                    g_w_to_plot = [gwObject for gwObject in self.gwObjects
                                   if gwObject.par in self.par]
                    g_w_pars = [g_w.par for g_w in g_w_to_plot]
                    sorted_g_w_to_plot = []
                    for par in self.par:
                        idx = g_w_pars.index(par)
                        sorted_g_w_to_plot.append(g_w_to_plot[idx])
                    # delete the unordered list of graph widgets
                    del g_w_to_plot

                    counter = 0
                    for i in range(self.nrows):
                        for j in range(self.ncols):
                            self.scroll_grid_layout.addWidget(
                                sorted_g_w_to_plot[counter], i, j)
                            # call the show method on the graphWidget object in order to
                            # display it
                            sorted_g_w_to_plot[counter].show()
                            # don't bother iterating to plot if all the parameters have been
                            # plotted else you'll get an error
                            if counter == len(sorted_g_w_to_plot) - 1 :
                                break
                            counter += 1
                    del sorted_g_w_to_plot

            self.ps.close()

    def editParamDef(self):
        global currPar, fit_par
        parIndex = self.par.index(currPar)
        user_input = self.ps.parameter.currentText()
        if (user_input and
            not str.upper(str(user_input)) in self.par):
            try:
                self.parVals[self.par[parIndex]]
            except KeyError:
                QtWidgets.QMessageBox.information(self, "Information",
                                                  "This parameter does not exist. Add to"
                                                  "view it.")
            else:
                user_input = str.upper(str(user_input))
                self.par[parIndex] = user_input
                unitMeas = str(self.ps.unitMeasurement.text())
                if user_input not in fit_par.keys():
                    fit_par[user_input] = unitMeas
                    for graph_widget in self.gwObjects:
                        if graph_widget.par == user_input:
                            graph_widget.unitMeas = unitMeas
                            break

                g_w_to_plot = [gwObject for gwObject in self.gwObjects
                               if gwObject.par == user_input]
                curr_par_position_on_layout = (
                    self.scroll_grid_layout.getItemPosition(parIndex))
                row_number = curr_par_position_on_layout[0]
                column_number = curr_par_position_on_layout[1]
                widget_to_remove = self.scroll_grid_layout.itemAt(parIndex).widget()
                self.scroll_grid_layout.removeWidget(widget_to_remove)
                widget_to_remove.close() # will this make me lose values of tilted-ring parameters?
                self.scroll_grid_layout.addWidget(g_w_to_plot[0], row_number,
                                                  column_number)
                # TODO 03/07/19 (sam): will be nice to add a little close icon on each graph widget
                # and then implement removeWidget and close functions when it's clicked 
                self.ps.close()
    
    def create_parameter_dialog(self, opt, title):
        global selected_option
        selected_option = opt
        val = []
        for i in self.parVals:
            if i in self.par:
                continue
            else:
                val.append(i)
        self.ps = ParamSpec(val, title)
        self.ps.show()
        self.ps.btnOK.clicked.connect(self.paramDef)
        self.ps.btnCancel.clicked.connect(self.ps.close)

    def add_parameter_dialog(self):
        selected_option = 'add'
        title = 'Add Parameter'
        self.create_parameter_dialog(selected_option, title)

    def insert_parameter_dialog(self):
        selected_option = 'insert'
        title = 'Insert Parameter'
        self.create_parameter_dialog(selected_option, title)

    def editParaObj(self):
        val = []
        for i in self.parVals:
            if i in self.par:
                continue
            else:
                val.append(i)

        self.ps = ParamSpec(val, "Edit Parameter")
        self.ps.show()
        self.ps.btnOK.clicked.connect(self.editParamDef)
        self.ps.btnCancel.clicked.connect(self.ps.close)

    def tirificMessage(self):
        """Displays the information about input data cube not available

        Keyword arguments:
        self--  main window being displayed i.e. the current instance of the
                mainWindow class

        Returns:
        None

        Displays a messagebox that informs user that changes have been successfully
        written to the .def file
        """
        QtWidgets.QMessageBox.information(self, "Information",
                                          "Data cube ("+self.INSET+") specified at INSET"
                                          " doesn't exist in specified directory.")

    def progressBar(self, cmd):
        progress = QtWidgets.QProgressDialog("Operation in progress...",
                                             "Cancel", 0, 100)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMaximum(self.loops*1e6)
        progress.resize(500, 100)
        prev = 1
        message = "Stopped"
        completed = int(prev * 1e6) / 2
        status = 'running'
        progress.show()
        time.sleep(10)
        while cmd.poll() is None and status == 'running':
            with open(self.progressPath, 'r') as f:
                data = f.readlines()
                for i in data:
                    lin = i.split(" ")
                    if 'L:' in lin[0].upper():
                        count = lin[0].split(":")
                        count = count[1].split("/")
                        if int(count[0]) > prev:
                            if int(count[0]) == self.loops:
                                completed += 0.0001
                            else:
                                prev = int(count[0])
                                completed = prev * 1e6
                        else:
                            completed += 0.0001
                    elif "finish" in lin[0].lower():
                        status = 'finished'
                        progress.setValue(self.loops * 1e6)
                        message = i
                        break
            progress.setValue(completed)
            if progress.wasCanceled():
                cmd.kill()
                break
        progress.setValue(self.loops * 1e6)
        QtWidgets.QMessageBox.information(self, "Information", message)

    def startTiriFiC(self):
        """Start TiRiFiC

        Keyword arguments:
        self--  main window being displayed i.e. the current instance of
        the mainWindow class

        Returns:
        None

        Calls the os.system and opens terminal to start TiRiFiC
        """
        fitsfilePath = os.getcwd()
        fitsfilePath = fitsfilePath + "/" + self.INSET
        if os.path.isfile(fitsfilePath):
            for i in self.gwObjects:
                self.saveFile(
                    i.parVals, i.par, i.unitMeas, i.numPrecisionX, i.numPrecisionY)

            tmpFile = []
            with open(self.fileName, 'a') as f:
                for i in self.data:
                    lineVals = i.split("=")
                    if len(lineVals) > 1:
                        lineVals[0] = ''.join(lineVals[0].split())
                        if lineVals[0] == "ACTION":
                            tmpFile.append("ACTION = 1\n")
                        elif lineVals[0] == "PROMPT":
                            tmpFile.append("PROMPT = 0\n")
                        elif lineVals[0] == "GR_DEVICE":
                            tmpFile.append(i)
                            tmpFile.append("GR_CONT = \n")
                        elif lineVals[0] == "PROGRESSLOG":
                            tmpFile.append("PROGRESSLOG = progress\n")
                        elif lineVals[0] == "GR_CONT":
                            pass
                        else:
                            tmpFile.append(i)
                    else:
                        tmpFile.append(i)

                f.seek(0)
                f.truncate()
                for i in tmpFile:
                    f.write(i)
            try:
                cmd = run(["tirific", "deffile=", self.fileName])
            except OSError:
                QtWidgets.QMessageBox.information(self, "Information",
                                                  "TiRiFiC is not installed or configured"
                                                  " properly on system.")
            else:
                self.progressPath = str(self.fileName)
                self.progressPath = self.progressPath.split('/')
                self.progressPath[-1] = 'progress'
                self.progressPath = '/'.join(self.progressPath)
                self.progressBar(cmd)
        else:
            self.tirificMessage()

def logWarnings():
    # logging.captureWarnings(True)
    # logging.basicConfig(filename='test.log', format='%(asctime)s %(name)s %(levelname)s %(message)s',
    #                     datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    logger = logging.getLogger(__name__)
    # warnings_logger = logging.getLogger("py.warnings")

    formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger_file_handler = logging.FileHandler('TiRiFiG.log', mode='a')
    logger_file_handler.setFormatter(formatter)

    logger.addHandler(logger_file_handler)
    # warnings_logger.addHandler(logger_file_handler)
    # logger.setLevel(logging.DEBUG)
    # warnings_logger.setLevel(logging.DEBUG)

def main():
    logWarnings()
    if os.path.isfile(os.getcwd() + "/tmpDeffile.def"):
        os.remove(os.getcwd() + "/tmpDeffile.def")

    app = QtWidgets.QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
