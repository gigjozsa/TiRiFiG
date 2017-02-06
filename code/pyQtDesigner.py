## -*- coding: utf-8 -*-
#
## Form implementation generated from reading ui file 'pyQtDesigner.ui'
##
## Created by: PyQt4 UI code generator 4.12
##
## WARNING! All changes made in this file will be lost!
#
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import sys
from math import ceil as mCeil
from PyQt4 import QtCore, QtGui

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
xScale=[]
yScale=[]
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

#Ui_MainWindow.file_open()
mPress=[-5+min(RADI)];mRelease=['None'];mMotion=[-5+min(RADI)]


parVals = {'RADI':RADI[:],'VROT':VROT[:]}

#app = Ui_MainWindow()


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
            
            
            
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def file_open(self):
        global fileName,data,VROT,RADI,historyList,xScale,yScale,key,numPrecisionY,numPrecisionX,app,par,NUR
        
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        fileName = open(name,'r')
        
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
        else:
            global app
            if len(VROT)==0:
                sys.exit(app.exec_())
                
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(663, 514)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 10, 211, 20))
        self.label.setObjectName(_fromUtf8("label"))
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 663, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuRun = QtGui.QMenu(self.menubar)
        self.menuRun.setObjectName(_fromUtf8("menuRun"))
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStatusTip('Open File')
        self.actionOpen.triggered.connect(self.file_open)
        
#        openFile = QtGui.QAction("&Open File", self)
#        openFile.setShortcut("Ctrl+O")
#        openFile.setStatusTip('Open File')
#        openFile.triggered.connect(self.file_open)
        
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionExit_2 = QtGui.QAction(MainWindow)
        self.actionExit_2.setObjectName(_fromUtf8("actionExit_2"))
        self.actionScale_Manager = QtGui.QAction(MainWindow)
        self.actionScale_Manager.setObjectName(_fromUtf8("actionScale_Manager"))
        self.actionPrecision = QtGui.QAction(MainWindow)
        self.actionPrecision.setObjectName(_fromUtf8("actionPrecision"))
        self.actionParameter = QtGui.QAction(MainWindow)
        self.actionParameter.setObjectName(_fromUtf8("actionParameter"))
        self.actionOpen_in_Editor = QtGui.QAction(MainWindow)
        self.actionOpen_in_Editor.setObjectName(_fromUtf8("actionOpen_in_Editor"))
        self.actionOpen_in_Editor_2 = QtGui.QAction(MainWindow)
        self.actionOpen_in_Editor_2.setObjectName(_fromUtf8("actionOpen_in_Editor_2"))
        self.actionStart_TiRiFiC = QtGui.QAction(MainWindow)
        self.actionStart_TiRiFiC.setObjectName(_fromUtf8("actionStart_TiRiFiC"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit_2)
        self.menuFile.addSeparator()
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionScale_Manager)
        self.menuEdit.addAction(self.actionPrecision)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionParameter)
        self.menuRun.addSeparator()
        self.menuRun.addAction(self.actionOpen_in_Editor_2)
        self.menuRun.addAction(self.actionStart_TiRiFiC)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Qt Tut", None))
        self.label.setText(_translate("MainWindow", "Viewgraph of VROT and RADI", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuRun.setTitle(_translate("MainWindow", "Run", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionSave_As.setText(_translate("MainWindow", "Save As", None))
        self.actionExit_2.setText(_translate("MainWindow", "Exit", None))
        self.actionScale_Manager.setText(_translate("MainWindow", "Scale Manager", None))
        self.actionPrecision.setText(_translate("MainWindow", "Precision", None))
        self.actionParameter.setText(_translate("MainWindow", "Parameter", None))
        self.actionOpen_in_Editor.setText(_translate("MainWindow", "Open in Editor", None))
        self.actionOpen_in_Editor_2.setText(_translate("MainWindow", "Open in Editor", None))
        self.actionStart_TiRiFiC.setText(_translate("MainWindow", "Start TiRiFiC", None))


if __name__ == "__main__":
#    import sys
    app = QtGui.QApplication(sys.argv)
    ani = animation.FuncAnimation(f, animate, interval=500)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #app.geometry("1280x720")
    MainWindow.show()
    sys.exit(app.exec_())


