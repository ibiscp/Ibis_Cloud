import os
import tkinter as tk
import tkinter.filedialog as tkfd
#import Tkinter as tk
import subprocess
#import tkFileDialog as tkfd
import database
import sys
import mainGui
import operator
import sync

from functools import partial

from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui

sourceDir = ''
destinationDir = ''
data = []
editing = False
ipAddress = ''
user = ''

class MainDialog(QDialog, mainGui.Ui_MainWindow):

    def __init__(self, parent=None):
        global data, ipAddress, user

        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        self.connect(self.sourceButton, SIGNAL("clicked()"), partial(self.openFolderDialog, 'source'))
        self.connect(self.destinationButton, SIGNAL("clicked()"), partial(self.openFolderDialog, 'destination'))
        self.connect(self.addButton, SIGNAL("clicked()"), self.saveMap)
        self.connect(self.tableView, SIGNAL("clicked(QModelIndex)"), self.rowSelected)
        self.connect(self.syncButton, SIGNAL("clicked()"), self.sync)
        self.connect(self.deleteButton, SIGNAL("clicked()"), self.deleteEntry)
        self.connect(self.sourceEdit, SIGNAL("textChanged(QString)"), partial(self.editTextChanged, 'source'))
        self.connect(self.destinationEdit, SIGNAL("textChanged(QString)"), partial(self.editTextChanged, 'destination'))
        self.connect(self.syncAllButton, SIGNAL("clicked()"), self.syncAll)
        self.connect(self.editButton, SIGNAL("clicked()"), self.edit)
        self.setWindowIcon(QIcon('ibisCloud.png'))

        # Create tray icon
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.activated.connect(self.iconActivated)
        self.trayIcon.setToolTip('Ibis Cloud')
        self.trayIcon.show()

        self.addButton.setEnabled(False)

        model = QFileSystemModel();
        model.setRootPath(QDir.currentPath())
        model.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)

        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(QDir.currentPath()))
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.treeView.expandsOnDoubleClick()

        self.treeView.show()
        self.treeView.expandAll()
        #Get server data
        data = database.GetServerData()
        ipAddress = data[0]
        user = data[1]

        #Get map data
        data = database.GetMap()

        i=0
        for row in data:
            row = list(row)
            row.append('Not Synced')
            data[i] = row
            i+=1

        self.updateTable()
        self.tableView.resizeColumnsToContents()

    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.showNormal()

    def showMessage(self, duration, icon, message):
        #duration = 3
        #icon = QtGui.QSystemTrayIcon.Information
        # self.trayIcon.showMessage('Ibis Cloud',
        #         'Don\'t worry, your files will remain synchronized.', icon,
        #         duration * 1000)
        self.trayIcon.showMessage('Ibis Cloud',
            message, icon,
            duration * 1000)

    # Create tray actions
    def createActions(self):
        # self.minimizeAction = QtGui.QAction("Mi&nimize", self,
        #         triggered=self.hide)

        # self.maximizeAction = QtGui.QAction("Ma&ximize", self,
        #         triggered=self.showMaximized)

        self.restoreAction = QtGui.QAction("&Restore", self,
                triggered=self.showNormal)

        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=QtGui.qApp.quit)

    # Create tray icon and its options
    def createTrayIcon(self):
         self.trayIconMenu = QtGui.QMenu(self)
         # self.trayIconMenu.addAction(self.minimizeAction)
         # self.trayIconMenu.addAction(self.maximizeAction)
         self.trayIconMenu.addAction(self.restoreAction)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)

         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setIcon(QIcon('ibisCloud.png'))
         self.trayIcon.setContextMenu(self.trayIconMenu)

    # Software closed
    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            self.showMessage(3, QtGui.QSystemTrayIcon.Information, 'Don\'t worry, your files will remain synchronized.')
            self.hide()
            event.ignore()

    # Textbox text changed
    def editTextChanged(self, buttonName, path):
        global sourceDir, destinationDir

        if (buttonName == 'source'):
            sourceDir = path

        elif (buttonName == 'destination'):
            destinationDir = path

        self.enableAddButton()

    # Map deleted
    def deleteEntry(self):
        global data

        #TODO Stop synchronization if synced

        row = self.getSelectedRow()
        id = data[row][0]

        database.deleteMapEntry(id)

        data = list(data)
        data.remove(data[row])

        self.updateTable()

    # Execute when a table entry is selected
    def rowSelected(self):
        global data

        #Enable Buttons
        self.enableButtons()

        row = self.getSelectedRow()

        if data[row][3] == 'Synced':
            self.syncButton.setText(QtGui.QApplication.translate("MainWindow", "Stop Sync", None, QtGui.QApplication.UnicodeUTF8))
        else:
            self.syncButton.setText(QtGui.QApplication.translate("MainWindow", "Start Sync", None, QtGui.QApplication.UnicodeUTF8))

    #Enable Buttons
    def enableButtons(self):
        self.syncButton.setEnabled(True)
        self.editButton.setEnabled(True)
        self.deleteButton.setEnabled(True)

    #Disable Buttons
    def disableButtons(self):
        self.syncButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.deleteButton.setEnabled(False)

    # Return the selected
    def getSelectedRow(self):
        rows=[]
        for idx in self.tableView.selectedIndexes():
                rows.append(idx.row())

        return rows[0]

    # Enable Add button if possible
    def enableAddButton(self):
        if (self.sourceEdit.text() != '' and self.destinationEdit.text() != ''):
            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)

    # Button Edit clicked
    def edit(self):
        global editing, sourceDir, destinationDir, data

        editing = True
        self.disableButtons()

        row = self.getSelectedRow()

        sourceDir = data[row][1]
        destinationDir = data[row][2]

        self.setText()

    # Button Start Sync clicked
    def sync(self):
        global data

        row = self.getSelectedRow()

        if data[row][3] == 'Synced':
            #TODO Implement Stop Sync
            data[row][3] = 'Not Synced'
        else:
            #TODO Implement Sync
            data[row][3] = 'Synced'

        self.rowSelected()
        self.updateTable()

    # Button Sync All clicked
    def syncAll(self):
        global data

        for row in data:
            if row[3] == 'Not Synced':
                #TODO Implement Sync
                row[3] = 'Synced'
                print(row)

        #self.rowSelected()
        self.updateTable()

    # Update the data table
    def updateTable(self):
        global data

        #Disable Buttons
        self.disableButtons()

        header=["Source", "Destination", "Status"]
        table_model = MyTableModel(self, data, header)
        self.tableView.setModel(table_model)

    # Save map in the database
    def saveMap(self):
        global sourceDir, destinationDir, data, editing, user, ipAddress

        # check if path exists and if folder is created
        print(os.path.isdir(sourceDir))
        print(os.path.exists(sourceDir))

        destinationDir = destinationDir.replace('Server/', '[user]@[ip]' + ':Data/')

        if (editing == True):
            row = self.getSelectedRow()
            id = data[row][0]

            database.UpdateMap([sourceDir, destinationDir, str(id)])

            editing = False
        else:
            database.AddMap([sourceDir, destinationDir])

        sourceDir = ''
        destinationDir = ''

        data = database.GetMap()
        i=0
        for row in data:
            row = list(row)
            row.append('Not Synced')
            data[i] = row
            i+=1

        self.setText()
        self.updateTable()
        self.enableAddButton()

    # Open folder dialog to chose Source/Destination
    def openFolderDialog(self, buttonName):
        global sourceDir, destinationDir, ipAddress, user
        root = tk.Tk()
        root.withdraw()

        rootFolder = repr(os.getcwd())
        rootFolder = rootFolder.replace("\\\\", "\\").replace("'", '')
        rootFolder += '\Folder_Structure'

        if (buttonName == 'source'):
            temp = sourceDir
            sourceDir = tkfd.askdirectory(parent=root,initialdir="/",title='Please select the source directory')

            if (sourceDir == ''):
                sourceDir = temp

        elif (buttonName == 'destination'):
            temp = destinationDir
            destinationDir = 'a'

            # Download the folder structure from the server
            #try:
            cmd = 'rsync -a -v -z -ssh --delete --delete-excluded ' + '-f"+ */" -f"- *" ' + user + '@' + ipAddress + ':Data/ ' + sync.convertPathToCygdrive(rootFolder)

            print (cmd)
            #TODO insert

            proc = subprocess.Popen(cmd,
              shell=True,
              stdin=subprocess.PIPE,
              stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT,
            )
            remainder = str(proc.communicate()[0])
            ibis = remainder.replace('\\n', '\n')
            #print(remainder)
            print(ibis)
            # output = ''
            # while not 'password' in output:
            #     output = proc.stdout.readline()
            #     print(output)
            # proc.stdin.write('ibiscp')
            #except:
            #    self.showMessage(3, QtGui.QSystemTrayIcon.Warning, 'Folder structure could not update!')

            while (not rootFolder in destinationDir) and (destinationDir != ''):
                destinationDir = tkfd.askdirectory(parent=root,initialdir=rootFolder,title='Please select the destination directory inside the folder: ' + rootFolder)
                destinationDir = destinationDir.replace("/", "\\")

            if (destinationDir == ''):
                destinationDir = temp

            # Change the folder path to server path
            destinationDir = 'Server/' + destinationDir[(len(rootFolder)+1):]

        self.setText()
        self.enableAddButton()

    # Update Source/Destination
    def setText(self):
        global sourceDir, destinationDir

        self.sourceEdit.setText(sourceDir)
        self.destinationEdit.setText(destinationDir)

class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        global ipAddress
        QAbstractTableModel.__init__(self, parent, *args)
        data = []
        if not len(mylist) == 0:
            for i in mylist:
                i[2] = i[2].replace('[user]@[ip]:Data/', 'Server/')
                data.append(i[1:])
        self.mylist = data
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))

app = QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()