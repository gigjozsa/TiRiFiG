import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(50,50,500,300)
        self.setWindowTitle("PyQT Tuts")
        

        extractAction = QtGui.QAction("Get to the Choppa!",self)        
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Leave the App")
        extractAction.triggered.connect(self.close_application)        
        
        self.statusBar()
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        fileMenu.addAction(extractAction)
        
        
        self.home()
        
    def home(self):
        btn = QtGui.QPushButton("Quit",self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(100,100)
        
        extractAction = QtGui.QAction(QtGui.QIcon)
        
        
        self.show()
        
        
    def close_application(self):
        print ("Pretty cool")
        sys.exit()
#        self.setWindowTitle("Today is Today")
        
        

def run():       
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    
run()