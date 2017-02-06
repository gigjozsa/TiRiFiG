# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 14:29:09 2017

@author: samuel
"""

import sys
from PyQt4 import QtGui

app = QtGui.QApplcation(sys.argv) 
window = QtGui.QWidget()
window.setGeometry(0,0,500,300)
window.setWindowTitle("PyQT Tuts!")
window.show()
sys.exit(app.exec_())