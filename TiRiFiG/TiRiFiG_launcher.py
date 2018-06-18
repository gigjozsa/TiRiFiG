#!/usr/bin/env python
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
            scaleChange    (bool):         determines whether or not scale has been
                                           changed.
            redo           (list):         the state of some parameters before undo
                                           action.
            mPress         (list):         x-y values of mouse click.
            mRelease       (list):         x-y values of mouse release.
            mMotion        (list):         x-y values of mouse motion.
            mDblPress      (list):         x-y values of mouse double click.

        Instance variables:
            xScale         (list):         upper and lower limit of x-axis.
            yScale         (list):         upper and lower limit of y-axis.
            choice         (string):       binary value which determines scale behaviour.
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
            gwDict         (dictionary):   filtered dictionary with only y-scale and
                                           choice value for each parameter.
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
            radioFree      (QRadioButton): specifying behaviour of viewgraph as "free".
            radioViewG     (QRadioButton): specify behaviour of viewgraph as "beyond
                                           viewgraph".
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
            choice          (string):      scale behaviour of viewgraph as points are
                                           dragged (free/beyond viewgraph).
            INSET           (string):      name of data cube retrieved from .def file.
            par             (list):        list of tilted-ring parameters.
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
            paraObj:                       instantiates the parameter specfication class and
                                           connects btnOK to paramDef function.
            editParaObj:                   instantiates the parameter specfication class and
                                           connects btnOK to editParamDef function.
            paramDef:                      adds specified paramater viewgraph to layout.
            editParamDef:                  changes the parameter plotted in viewgraph to
                                           the specified parameter.
            tirificMessage:                displays information about input data cube not
                                           available in current working directory.
            startTiriFiC:                  starts TiRiFiC from terminal.
"""

#libraries
import os, sys, threading, time
from subprocess import Popen as run
from math import ceil
from decimal import Decimal
import numpy as np
#matplotlib.use("qt4Agg")
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from PyQt4 import QtGui, QtCore

currPar = None
fit_par = {'SBR':'Jy km s-1 arcsec-2', 'RADI':'arcsec', 'VROT':'km s-1', 'Z0':'arcsec',
           'SDIS':'km s-1', 'INCL':'degrees', 'PA':'degrees', 'XPOS':'degrees',
           'YPOS':'degrees', 'VSYS':'km s-1', 'DVRO':'km s-1 arcsec-1',
           'DVRA':'km s-1 arcsec-1', 'VRAD': 'km s-1'}

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
    cp = QtGui.QDesktopWidget().availableGeometry().center()
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

class GraphWidget(QtGui.QWidget):
    scaleChange = "No"
    redo = []
    mPress = [None, None]
    mRelease = [None, None]
    mMotion = [None]
    mDblPress = [None, None]

    def __init__(self, parent, xScale, yScale, choice, unitMeas, par, parVals, parValRADI,
                 historyList, key, numPrecisionX, numPrecisionY):
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

        #Grid Layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        #Canvas and Toolbar
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

        #change the parameter in the viewgraph
        self.btnAddParam = QtGui.QPushButton('&Add', self)
        self.btnAddParam.setFixedSize(50, 30)
        self.btnAddParam.setFlat(True)
        # FIX ME: use icon instead of text
        # self.btnAddParam.setIcon(QtGui.QIcon('utilities/icons/plus.png'))
        self.btnAddParam.setToolTip('Add Parameter')

        # modify plotted parameter
        self.btnEditParam = QtGui.QPushButton('&Change', self)
        self.btnEditParam.setFixedSize(50, 30)
        self.btnEditParam.setFlat(True)
        # FIX ME: use icon instead if text
        # self.btnEditParam.setIcon(QtGui.QIcon('utilities/icons/edit.png'))
        self.btnEditParam.setToolTip('Modify plotted parameter')

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.btnAddParam)
        hbox.addWidget(self.btnEditParam)

        grid.addLayout(hbox, 0, 0)
        grid.addWidget(self.canvas, 2, 0, 1, 2)

        self.firstPlot()

    def changeGlobal(self):
        global currPar
        currPar = self.par


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
            text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                                  'Enter new node value:')

            if ok:
                if text:
                    newVal = int(str(text))
                    for j in range(len(self.parValRADI)):
                        if (
                                (self.mDblPress[0] < (self.parValRADI[j])+3) and
                                (self.mDblPress[0] > (self.parValRADI[j])-3) and
                                (self.mDblPress[1] < (self.parVals[j])+3) and
                                (self.mDblPress[1] > (self.parVals[j])-3)
                            ):

                            self.parVals[j] = newVal

                            self.ax.clear()
                            self.ax.set_xlim(self.xScale[0], self.xScale[1])

                            if np.subtract(max(self.parVals), min(self.parVals)) == 0:
                                self.yScale = [-100, 100]
                            elif (max(self.parVals) - min(self.parVals)) <= 100:
                                self.yScale = [int(ceil(-2 * max(self.parVals))),
                                               int(ceil(2 * max(self.parVals)))]
                            else:
                                self.yScale = [
                                    int(ceil(min(self.parVals) -
                                             0.1 * (max(self.parVals) -
                                                    min(self.parVals)))),
                                    int(ceil(max(self.parVals) +
                                             0.1 * (max(self.parVals) -
                                                    min(self.parVals))))]

                            self.ax.set_xlabel("RADI (arcsec)")
                            self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                            self.ax.plot(self.parValRADI, self.parVals, '--bo')
                            # self.ax[i].set_title('Plot')
                            self.ax.set_xticks(self.parValRADI)
                            # plt.tight_layout()
                            self.canvas.draw()
                            self.key = "No"
                            break



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
        # whilst the left mouse button is being clicked and mouse pointer hasnt
        # (why not use mPress=None instead of event.button = 1)
        # moved out of the figure canvas, capture the VROT (y-value) during mouse
        # movement and call re-draw graph

        if event.button == 1 and not event.ydata is None:
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
            self.redo.append([self.scaleChange, self.choice, self.numPrecisionY,
                              self.parVals[:], self.historyList[-1], self.yScale[:]])
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
            self.scaleChange = self.redo[-1][0]
            self.choice = self.redo[-1][1]
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
        QtGui.QMessageBox.information(self, "Information", "History list is exhausted")


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
        # self.ax.set_ylim(self.yScale[0], self.yScale[1])
        self.ax.set_xlabel("RADI (arcsec)")
        self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
        self.ax.plot(self.parValRADI, self.historyList[-1], '--bo')
        # self.ax.set_title('RADI by %s'%self.par)
        self.ax.set_xticks(self.parValRADI)
        # plt.tight_layout()
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

        if self.scaleChange == "Yes":

            for i in range(len(self.par)):
                self.ax[i].clear()
                self.ax[i].set_xlim(self.xScale[0], self.xScale[1])
                if (max(self.parVals[self.par[i]]) -
                        min(self.parVals[self.par[i]])) <= 100:
                    self.yScale[self.par[i]] = [
                        int(ceil(-2 * max(self.parVals[self.par[i]]))),
                        int(ceil(2 * max(self.parVals[self.par[i]])))]
                else:
                    self.yScale[self.par[i]] = [
                        int(ceil(min(self.parVals[self.par[i]]) -
                                 0.1 * (max(self.parVals[self.par[i]]) -
                                        min(self.parVals[self.par[i]])))),
                        int(ceil(max(self.parVals[self.par[i]]) +
                                 0.1 * (max(self.parVals[self.par[i]]) -
                                        min(self.parVals[self.par[i]]))))
                        ]

                self.ax[i].set_ylim(self.yScale[self.par[i]][0],
                                    self.yScale[self.par[i]][1])
                self.ax[i].set_xlabel("RADI (arcsec)")
                self.ax[i].set_ylabel(self.par[i] + "( "+self.unitMeas[i]+ " )")
                self.ax[i].plot(
                    self.parVals['RADI'],
                    self.historyList[self.par[i]][len(self.historyList[self.par[i]])-1],
                    '--bo')
                # self.ax[i].set_title('Plot')
                self.ax[i].set_xticks(self.parVals['RADI'])

            # plt.tight_layout()
            self.canvas.draw()
            self.key = "No"

        if self.key == "Yes":
            self.firstPlot()

        # this re-plots the graph as long as the mouse is in motion and the right data
        # point is clicked
        else:
            for j in range(len(self.parValRADI)):
                if ((self.mPress[0] < (self.parValRADI[j]) + 3) and
                        (self.mPress[0] > (self.parValRADI[j]) - 3) and
                        (self.mRelease[0] is None)):
                   # and (self.mPress[1] < (self.parVals[j])+3) and
                   # (self.mPress[1] > (self.parVals[j])-3):
                    self.parVals[j] = self.mMotion[0]
                    self.ax.clear()
                    self.ax.set_xlim(self.xScale[0], self.xScale[1])
                    if self.choice == "Beyond Viewgraph":
                        if self.mMotion[0] >= 0.85*self.yScale[1]:
                            self.yScale = [int(ceil(min(self.parVals) -
                                                    0.1 * (max(self.parVals) -
                                                           min(self.parVals)))),
                                           int(ceil(max(self.parVals) +
                                                    0.1 * (max(self.parVals) -
                                                           min(self.parVals))))]
                        elif abs(self.mMotion[0]) <= abs(1.15 * self.yScale[0]):
                            self.yScale = [int(ceil(min(self.parVals) -
                                                    0.1 * (max(self.parVals) -
                                                           min(self.parVals)))),
                                           int(ceil(max(self.parVals) +
                                                    0.1 * (max(self.parVals) -
                                                           min(self.parVals))))]
                    elif self.choice == "Free":
                        if (max(self.parVals) - min(self.parVals)) <= 100:
                            self.yScale = [int(ceil(min(self.parVals)-
                                                    0.1 * (max(self.parVals) -
                                                           min(self.parVals)))),
                                           int(ceil(max(self.parVals) +
                                                    0.1 * (max(self.parVals) -
                                                           min(self.parVals))))]
                        else:
                            self.yScale = [int(ceil(min(self.parVals) -
                                                    0.1 * (max(self.parVals) -
                                                           min(self.parVals)))),
                                           int(ceil(max(self.parVals) +
                                                    0.1 * (max(self.parVals) -
                                                           min(self.parVals))))]

                    self.ax.set_xlabel("RADI (arcsec)")
                    self.ax.set_ylabel(self.par + "( "+self.unitMeas+ " )")
                    # self.ax.plot(self.parVals['RADI'],
                    # self.historyList[self.par][len(self.historyList[self.par])-1],'--bo')
                    self.ax.plot(self.parValRADI, self.parVals, '--bo')
                    # self.ax[i].set_title('Plot')
                    self.ax.set_xticks(self.parValRADI)
                    # plt.tight_layout()
                    self.canvas.draw()
                    self.key = "No"
                    break

class SMWindow(QtGui.QWidget):

    def __init__(self, par, xVal, gwDict):
        super(SMWindow, self).__init__()
        self.xMinVal = xVal[0]
        self.xMaxVal = xVal[1]
        # self.yMinVal = yVal[0]
        # self.yMaxVal = yVal[1]
        self.par = par
        self.gwDict = gwDict
        self.prevParVal = ""
        self.counter = 0

        self.parameter = QtGui.QComboBox()
        # self.parameter.setEditable(True)
        self.parameter.addItem("Select Parameter")
        for i in self.par:
            self.parameter.addItem(i)
        self.parameter.setAutoCompletion(True)
        self.parameter.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.parameter.setMaxVisibleItems(5)
        index = self.parameter.findText("Select Parameter", QtCore.Qt.MatchFixedString)
        self.parameter.setCurrentIndex(index)
        self.parameter.currentIndexChanged.connect(self.onChangeEvent)
        # run a for loop here to gather all they loaded parameters and populate as many text boxes

        self.xLabel = QtGui.QLabel("RADI")
        self.xMin = QtGui.QLineEdit()
        self.xMin.setPlaceholderText("RADI min ("+str(self.xMinVal)+")")
        self.xMax = QtGui.QLineEdit()
        self.xMax.setPlaceholderText("RADI max ("+str(self.xMaxVal)+")")
        self.xGrid = QtGui.QGridLayout()
        self.xGrid.setSpacing(10)
        self.xGrid.addWidget(self.xLabel, 1, 0)
        self.xGrid.addWidget(self.xMin, 2, 0)
        self.xGrid.addWidget(self.xMax, 2, 1)

        self.yMin = QtGui.QLineEdit()
        self.yMax = QtGui.QLineEdit()
        self.yGrid = QtGui.QGridLayout()
        self.yGrid.setSpacing(10)
        self.yGrid.addWidget(self.parameter, 1, 0)
        self.yGrid.addWidget(self.yMin, 2, 0)
        self.yGrid.addWidget(self.yMax, 2, 1)

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
        # self.btnCancel.clicked.connect(self.close)
        self.hboxBtns.addWidget(self.btnUpdate)
        self.hboxBtns.addWidget(self.btnCancel)

        self.fbox = QtGui.QFormLayout()
        self.fbox.addRow(self.xGrid)
        self.fbox.addRow(self.yGrid)
        # self.fbox.addRow(self.parameter)
        # self.fbox.addRow(self.yhbox)
        self.fbox.addRow(QtGui.QLabel("Scale Behaviour"), self.hbox)
        self.fbox.addRow(self.hboxBtns)

        self.setLayout(self.fbox)
        self.setFocus()
        self.setWindowTitle("Scale Manager")
        self.setGeometry(300, 300, 300, 150)
        _center(self)
        self.setFocus()

    def onChangeEvent(self):

        if self.yMin.text():
            self.gwDict[self.prevParVal][0][0] = int(str(self.yMin.text()))
            self.gwDict[self.prevParVal][0][1] = int(str(self.yMax.text()))
            choice = "Free" if self.radioFree.isChecked() else "Beyond Viewgraph"
            self.gwDict[self.prevParVal][1] = choice

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

    def __init__(self, par, windowTitle):
        super(ParamSpec, self).__init__()
        self.par = par

        self.parameterLabel = QtGui.QLabel("Parameter")
        self.parameter = QtGui.QComboBox()
        self.parameter.setEditable(True)
        self.parameter.addItem("Select Parameter")
        for i in self.par:
            self.parameter.addItem(i)
        self.parameter.setAutoCompletion(True)
        self.parameter.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.parameter.setMaxVisibleItems(6)
        index = self.parameter.findText("Select Parameter", QtCore.Qt.MatchFixedString)
        self.parameter.setCurrentIndex(index)


        self.uMeasLabel = QtGui.QLabel("Unit Measurement")
        self.unitMeasurement = QtGui.QLineEdit()
        # self.unitMeasurement.setPlaceholderText("Unit Measurement")

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

        self.grid.addLayout(self.hbox, 3, 1)
        self.setLayout(self.grid)

        self.setWindowTitle(windowTitle)
        self.setGeometry(300, 300, 300, 150)

        _center(self)
        self.setFocus()



class MainWindow(QtGui.QMainWindow):
    runNo = 0
    key = "Yes"
    loops = 0
    ncols = 1; nrows = 4
    choice = "Beyond Viewgraph"
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
        self.cWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.cWidget)
        self.vLayout = QtGui.QVBoxLayout(self.cWidget)
        # you can ignore the parent and it will still work
        btnOpen = QtGui.QPushButton('&Open File', self.cWidget)
        btnOpen.setFixedSize(80, 30)
        # btnOpen.setFlat(True)
        btnOpen.setToolTip('Open .def file')
        btnOpen.clicked.connect(self.openDef)
        self.vLayout.addWidget(btnOpen)
        # you can ignore the parent and it will still work
        self.scrollArea = QtGui.QScrollArea(self.cWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContent = QtGui.QWidget(self.scrollArea)
        self.gridLayoutScroll = QtGui.QGridLayout(self.scrollAreaContent)
        self.scrollArea.setWidget(self.scrollAreaContent)
        self.vLayout.addWidget(self.scrollArea)
        self.createActions()
        self.createMenus()

    def createActions(self):
        self.exitAction = QtGui.QAction("&Exit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip('Leave the app')
        self.exitAction.triggered.connect(self.quitApp)

        self.openFile = QtGui.QAction("&Open File", self)
        self.openFile.setShortcut("Ctrl+O")
        self.openFile.setStatusTip('Load .def file to be plotted')
        self.openFile.triggered.connect(self.openDef)

        self.saveChanges = QtGui.QAction("&Save", self)
        self.saveChanges.setStatusTip('Save changes to .def file')
        self.saveChanges.triggered.connect(self.saveAll)

        self.saveAsFile = QtGui.QAction("&Save as...", self)
        self.saveAsFile.setStatusTip('Create another .def file with current '
                                     'paramater values')
        self.saveAsFile.triggered.connect(self.saveAsAll)

        self.undoAction = QtGui.QAction("&Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.setStatusTip('Undo last action')
        self.undoAction.triggered.connect(self.undoCommand)

        self.redoAction = QtGui.QAction("&Redo", self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.setStatusTip('Redo last action')
        self.redoAction.triggered.connect(self.redoCommand)

        self.openTextEditor = QtGui.QAction("&Open Text Editor...", self)
        self.openTextEditor.setStatusTip('View the current open .def file in '
                                         'preferred text editor')
        self.openTextEditor.triggered.connect(self.openEditor)

        self.startTF = QtGui.QAction("&Start TiriFiC", self)
        self.startTF.setStatusTip('Starts TiRiFiC from terminal')
        self.startTF.triggered.connect(self.startTiriFiC)

        self.winSpec = QtGui.QAction("&Window Specification", self)
        self.winSpec.setStatusTip('Determines the number of rows and columns in a plot')
        self.winSpec.triggered.connect(self.setRowCol)

        self.scaleMan = QtGui.QAction("&Scale Manager", self)
        self.scaleMan.setStatusTip('Manages behaviour of scale and min and max values')
        self.scaleMan.triggered.connect(self.inProgress)

        self.paraDef = QtGui.QAction("&Parameter Definition", self)
        # self.paraDef.setStatusTip('Determines which parameter is plotted')
        self.paraDef.triggered.connect(self.paraObj)

        # self.sm.radioFree.clicked.connect(self.getOptF)
        # self.sm.radioViewG.clicked.connect(self.getOptV)
        # self.sm.btnUpdate.clicked.connect(self.updateScale)
        # self.sm.btnCancel.clicked.connect(self.sm.close)

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
        QtGui.qApp.quit()

    def cleanUp(self):

        # FIXME(Samuel 11-06-2018): Find a way to do this better

        self.key = "Yes"
        self.ncols = 1; self.nrows = 4
        self.choice = "Beyond Viewgraph"
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
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, "Open .def File", "~/",
                                                          ".def Files (*.def)")

        # assign texts of read lines to data variable if fileName is exists, else assign
        # None
        try:
            with open(self.fileName) as f:
                data = f.readlines()
        except:
            QtGui.QMessageBox.information(self, "Information",
                                          "Empty/Invalid file specified")
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
            QtGui.QMessageBox.information(self, "Information",
                                          "Tilted-ring parameters not retrieved")
        else:
            self.data = data
            if self.runNo > 0:
                # FIXME reloading another file on already opened not properly working
                # user has to close open window and reopen file for such a case
                QtGui.QMessageBox.information(self, "Information",
                                              "Close app and reopen to load file. Bug"
                                              "being fixed")
                # self.cleanUp()
                # FIXME (Samuel 11-06-2018): Find a better way to do this
                # self.data = data
                # self.getParameter(self.data)
            else:

                # defining the x scale for plotting
                if np.subtract(max(self.parVals['RADI']), min(self.parVals['RADI'])) == 0:
                    self.xScale = [-100, 100]
                elif (np.subtract(max(self.parVals['RADI']),
                                  min(self.parVals['RADI'])) <= 100):
                    self.xScale = [int(ceil(-2 * max(self.parVals['RADI']))),
                                   int(ceil(2 * max(self.parVals['RADI'])))]
                else:
                    self.xScale = [int(ceil(min(self.parVals['RADI']) -
                                            0.1 * (max(self.parVals['RADI']) -
                                                   min(self.parVals['RADI'])))),
                                   int(ceil(max(self.parVals['RADI']) +
                                            0.1 * (max(self.parVals['RADI']) -
                                                   min(self.parVals['RADI']))))]

                self.scrollWidth = self.scrollAreaContent.width()
                self.scrollHeight = self.scrollAreaContent.height()
                counter = 0
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

                    if np.subtract(max(self.parVals[key]), min(self.parVals[key])) == 0:
                        self.yScale[key] = [-100, 100]
                    elif (max(self.parVals[key]) - min(self.parVals[key])) <= 100:
                        self.yScale[key] = [int(ceil(-2 * max(self.parVals[key]))),
                                            int(ceil(2 * max(self.parVals[key])))]
                    else:
                        self.yScale[key] = [int(ceil(min(self.parVals[key]) -
                                                     0.1 * (max(self.parVals[key]) -
                                                            min(self.parVals[key])))),
                                            int(ceil(max(self.parVals[key]) +
                                                     0.1 * (max(self.parVals[key]) -
                                                            min(self.parVals[key]))))]

                    unit = fit_par[key] if key in fit_par.keys() else ""
                    self.gwObjects.append(GraphWidget(self.scrollArea, self.xScale,
                                                      self.yScale[key][:],
                                                      self.choice,
                                                      unit, key,
                                                      self.parVals[key][:],
                                                      self.parVals['RADI'][:],
                                                      self.historyList[key][:],
                                                      self.key, self.numPrecisionX,
                                                      self.numPrecisionY[key]))
                    self.gwObjects[-1].btnAddParam.clicked.connect(
                        self.gwObjects[-1].changeGlobal)
                    self.gwObjects[-1].btnAddParam.clicked.connect(
                        self.paraObj)
                    self.gwObjects[-1].btnEditParam.clicked.connect(
                        self.gwObjects[-1].changeGlobal)
                    self.gwObjects[-1].btnEditParam.clicked.connect(
                        self.editParaObj)
                    self.gwObjects[-1].setMinimumSize(self.scrollWidth/2, self.scrollHeight/2)
                    if key in self.par:
                        self.gridLayoutScroll.addWidget(self.gwObjects[-1], counter, 0)
                    counter += 1
                self.runNo += 1

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
        text, ok = QtGui.QInputDialog.getText(self, 'Window number Input Dialog',
                                              'Specify the number of rows and columns (5,5):')
        if ok:
            if text:
                text = str(text)
                text = text.split(",")
                self.nrows = int(text[0])
                self.ncols = int(text[1])
                if (self.nrows * self.ncols) >= len(self.par):
                    # clear the existing graph objects before making new object for
                    # new grid
                    for i in reversed(range(self.gridLayoutScroll.count())):
                        self.gridLayoutScroll.itemAt(i).widget().setParent(None)

                    counter = 0
                    for i in range(self.nrows):
                        for j in range(self.ncols):
                            for k in range(counter, len(self.gwObjects)):
                                if self.gwObjects[k].par in self.par:
                                    self.gridLayoutScroll.addWidget(
                                        self.gwObjects[k], i, j)
                                    counter = k+1
                                    break
                else:
                    QtGui.QMessageBox.information(self, "Information",
                                                  "Product of Rows and Columns should"
                                                  "match the current number of parameters"
                                                  "on viewgraph")

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
        QtGui.QMessageBox.information(self, "Information",
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
        QtGui.QMessageBox.information(self, "Information", "File Successfully Saved")

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
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save .def file as ",
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
        text, ok = QtGui.QInputDialog.getText(self, 'Text Editor Input Dialog',
                                              'Enter text editor:')

        if ok:

            for i in self.gwObjects:
                self.saveAs(self.tmpDeffile, i.parVals, i.par, i.unitMeas,
                            i.numPrecisionX, i.numPrecisionY)

            if text:
                programName = str(text)
                try:
                    run([programName, self.tmpDeffile])
                except OSError:
                    QtGui.QMessageBox.information(self, "Information",
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
        QtGui.QMessageBox.information(self, "Information",
                                      "This feature is under development")

    def SMobj(self):
        filtGwObj = {}
        for i in self.gwObjects:
            filtGwObj[i.par] = [i.yScale, i.choice]
        self.sm = SMWindow(self.par, self.xScale, filtGwObj)
        self.sm.show()
        self.sm.btnUpdate.clicked.connect(self.updateScale)
        self.sm.btnCancel.clicked.connect(self.sm.close)

    def updateScale(self):

        if len(self.sm.xMin.text()) > 0:
            self.sm.xMinVal = int(str(self.sm.xMin.text()))
            self.sm.xMaxVal = int(str(self.sm.xMax.text()))

        if len(self.sm.yMin.text()) > 0:
            self.sm.gwDict[self.sm.prevParVal][0][0] = int(str(self.sm.yMin.text()))
            self.sm.gwDict[self.sm.prevParVal][0][1] = int(str(self.sm.yMax.text()))
            choice = "Free" if self.sm.radioFree.isChecked() else "Beyond Viewgraph"
            self.sm.gwDict[self.sm.prevParVal][1] = choice

        argKeys = [i for i in self.sm.gwDict]
        counter = 0
        for i in self.gwObjects:
            if i.par == argKeys[counter]:
                i.yScale = self.sm.gwDict[argKeys[counter]][0]
                i.choice = self.sm.gwDict[argKeys[counter]][1]
                i.xScale = [self.sm.xMinVal, self.sm.xMaxVal]
                counter += 1
                # FIXME the first plot function should be invoked here
        self.sm.close
        QtGui.QMessageBox.information(self, "Information", "Done!")

    def paramDef(self):
        global currPar, fit_par
        parIndex = self.par.index(currPar)

        if (len(str(self.ps.parameter.currentText())) > 0 and
                not str.upper(str(self.ps.parameter.currentText())) in self.par):
            self.par.insert(parIndex + 1,
                            str.upper(str(self.ps.parameter.currentText())))
            unitMeas = str(self.ps.unitMeasurement.text())

            if self.par[parIndex + 1] not in self.parVals:
                zeroVals = []
                for i in range(self.NUR):
                    zeroVals.append(0.0)
                self.parVals[self.par[parIndex + 1]] = zeroVals[:]
                del zeroVals
                self.historyList[self.par[parIndex + 1]] = (
                    [self.parVals[self.par[parIndex + 1]][:]])
                self.yScale[self.par[parIndex + 1]] = [-100, 100]
                fit_par[self.par[parIndex+1]] = unitMeas
                self.gwObjects.insert(parIndex+1,
                                      GraphWidget(self.scrollArea,
                                                  self.xScale,
                                                  self.yScale[self.par[parIndex+1]],
                                                  self.choice,
                                                  unitMeas,
                                                  self.par[parIndex+1],
                                                  self.parVals[self.par[parIndex+1]],
                                                  self.parVals['RADI'],
                                                  self.historyList[self.par[parIndex+1]],
                                                  "Yes",
                                                  self.numPrecisionX,
                                                  1))
                self.gwObjects[parIndex+1].setMinimumSize(self.scrollWidth/2,
                                                          self.scrollHeight/2)
                self.gwObjects[parIndex+1].btnAddParam.clicked.connect(
                    self.gwObjects[parIndex+1].changeGlobal)
                self.gwObjects[parIndex+1].btnAddParam.clicked.connect(
                    self.paraObj)
                self.gwObjects[parIndex+1].btnEditParam.clicked.connect(
                    self.gwObjects[parIndex+1].changeGlobal)
                self.gwObjects[parIndex+1].btnEditParam.clicked.connect(
                    self.editParaObj)
            else:
                if self.par[parIndex + 1] not in fit_par.keys():
                    fit_par[self.par[parIndex + 1]] = unitMeas
                    for i in self.gwObjects:
                        if i.par == self.par[parIndex + 1]:
                            i.unitMeas = unitMeas
                            break
            self.nrows += 1
            for i in reversed(range(self.gridLayoutScroll.count())):
                self.gridLayoutScroll.itemAt(i).widget().setParent(None)

            counter = 0
            for i in range(self.nrows):
                for j in range(self.ncols):
                    for k in range(counter, len(self.par)):
                        for x in range(len(self.gwObjects)):
                            if self.gwObjects[x].par == self.par[k]:
                                self.gridLayoutScroll.addWidget(self.gwObjects[x], i, j)
                                counter = k + 1
                                break
                        break

            self.ps.close()

    def paraObj(self):

        val = []
        for i in self.parVals:
            if i in self.par:
                continue
            else:
                val.append(i)

        self.ps = ParamSpec(val, "Add Parameter")
        self.ps.show()
        self.ps.btnOK.clicked.connect(self.paramDef)
        self.ps.btnCancel.clicked.connect(self.ps.close)

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

    def editParamDef(self):
        global currPar
        parIndex = self.par.index(currPar)
        if (len(str(self.ps.parameter.currentText())) > 0 and
                not str.upper(str(self.ps.parameter.currentText())) in self.par):
            try:
                self.parVals[self.par[parIndex]]
            except KeyError:
                QtGui.QMessageBox.information(self, "Information",
                                              "This parameter does not exist. Add to"
                                              "view it.")
            else:
                self.par[parIndex] = str.upper(str(self.ps.parameter.currentText()))
                unitMeas = str(self.ps.unitMeasurement.text())
                if self.par[parIndex] not in fit_par.keys():
                    fit_par[self.par[parIndex]] = unitMeas
                    for i in self.gwObjects:
                        if i.par == self.par[parIndex]:
                            i.unitMeas = unitMeas
                            break

                for i in reversed(range(self.gridLayoutScroll.count())):
                    self.gridLayoutScroll.itemAt(i).widget().setParent(None)

                counter = 0
                for i in range(self.nrows):
                    for j in range(self.ncols):
                        for k in range(counter, len(self.par)):
                            for x in range(len(self.gwObjects)):
                                if self.gwObjects[x].par == self.par[k]:
                                    self.gridLayoutScroll.addWidget(self.gwObjects[x], i, j)
                                    counter = k + 1
                                    break
                            break

                self.ps.close()

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
        QtGui.QMessageBox.information(self, "Information",
                                      "Data cube ("+self.INSET+") specified at INSET"
                                      "doesn't exist in specified directory.")

    def progressBar(self, cmd):
        progress = QtGui.QProgressDialog("Operation in progress...",
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
        QtGui.QMessageBox.information(self, "Information", message)

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
                QtGui.QMessageBox.information(self, "Information",
                                              "TiRiFiC is not installed or configured"
                                              "properly on system.")
            else:
                self.progressPath = str(self.fileName)
                self.progressPath = self.progressPath.split('/')
                self.progressPath[-1] = 'progress'
                self.progressPath = '/'.join(self.progressPath)
                self.progressBar(cmd)
        else:
            self.tirificMessage()

def main():
    if os.path.isfile(os.getcwd() + "/tmpDeffile.def"):
        os.remove(os.getcwd() + "/tmpDeffile.def")

    app = QtGui.QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
