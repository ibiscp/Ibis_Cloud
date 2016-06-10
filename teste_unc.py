from win_unc import DiskDrive, UncDirectory, UncDirectoryMount, UncCredentials

# Describe your UNC path:
# Or provide credentials if you need them:
# creds = UncCredentials('ibis', 'ibiscp')
# authz_unc = UncDirectory(r'\\187.65.245.244', creds)
#
# # Setup a connection handler:
# conn = UncDirectoryMount(authz_unc)
# conn.mount()
#
# print "is mounted"
# print conn.disk_drive
#
# conn.unmount()
# assert(not conn.is_mounted())
#
#
#


# #from win_unc import UncDirectory, UncCredentials, UncDirectoryMount, DiskDrive
#
# __author__ = 'Ibis'
#
# # # Describe your UNC path:
# # simple_unc = UncDirectory(r'\\pedroperalta@no-ip.org')
# # #simple_unc = UncDirectory(r'\\home\shared')
# # creds = UncCredentials('ibis', 'ibiscp')
# # # Setup a connection handler:
# # conn = UncDirectoryMount(simple_unc, DiskDrive('Z:'), None, creds)
# # conn.mount()
#
# from win_unc import UncCredentials, UncDirectory, UncDirectoryConnection
#
# # # Describe your UNC path:
# simple_unc = UncDirectory(r"\\Ibis\Users")
#
# # # Or provide credentials if you need them:
# #creds = UncCredentials('ibis', 'ibiscp')
# #authz_unc = UncDirectory(r'\\187.65.245.244', creds)
#
# # Setup a connection handler:
# # conn = UncDirectoryConnection(simple_unc)
# # conn.connect()
#
# # import subprocess
# #
# # driveLetter = 'Q:'
# # networkPath = '\\\\'

import os
#import tkinter as tk
#import tkinter.filedialog as tkfd
import Tkinter as tk
import subprocess
import tkFileDialog as tkfd
import database
import sys
import mainGui
import operator
import sync

from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui

app = QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()

model = QFileSystemModel();
model.setRootPath(QDir.currentPath())
tree = QTreeView()
tree.setModel(model)
tree.setRootIndex(model.index(QDir.currentPath()))
tree.show()