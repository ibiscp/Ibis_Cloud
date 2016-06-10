#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

sourceDir = ''
destinationDir = ''

# Our main window
class MainWindow(QDeclarativeView):
   
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # Renders 'view.qml'
        self.setSource(QUrl.fromLocalFile('main.qml'))
        
        # QML resizes to main window
        self.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        #self.connect(self.source, SIGNAL("textChanged(QString)"), partial(self.editTextChanged, 'source'))

        # STYLING
        self.setWindowFlags(Qt.FramelessWindowHint)

    # Textbox text changed
    def editTextChanged(self, buttonName, path):
        global sourceDir, destinationDir

        if (buttonName == 'source'):
            sourceDir = path

        elif (buttonName == 'destination'):
            destinationDir = path

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the main window
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())