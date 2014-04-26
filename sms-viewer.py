#! /bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

##############################################
##                  GUI
##############################################

class MainWindow(QtGui.QMainWindow):
    def __init__(self,msgs):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle("Consultation SMS")
        self.resize(500, 600)

        self.centralwidget = QtGui.QWidget(self)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        
        self.verticalLayout = QtGui.QVBoxLayout()
        
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)

        self.gridLayout_2 = QtGui.QGridLayout(self.scrollArea)
        
        self.tableView = QtGui.QTableWidget(self.scrollArea)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.verticalHeader().setVisible(False)
        
        self.enterconv(msgs)

        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.scrollArea)

        self.pushButton = QtGui.QPushButton("Ok Go !",self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        #self.statusbar = QtGui.QStatusBar(self)
        #self.setStatusBar(self.statusbar)
        
        self.marandspa([self.gridLayout, self.gridLayout_2, self.verticalLayout])

    def marandspa(self,layouts):
        for layout in layouts:
            layout.setMargin(0)
            layout.setSpacing(0)

    def enterconv(self, msgs):
        
        entries = []

        for name in msgs.keys():
		    try:
			    int(name.split(';')[0])
		    except ValueError:
			    entries.append([_fromUtf8(name),len(msgs[name]), str(self.get_last_date(name)), self.get_last_msg(name)])


        self.tableView.setRowCount(len(entries))
        self.tableView.setColumnCount(len(entries[0]))

        for i, row in enumerate(entries):
            for j, col in enumerate(row):
                item = QtGui.QTableWidgetItem(col)
                if j==1:
                    item.setData(QtCore.Qt.EditRole, col)
                self.tableView.setItem(i, j, item)
        
        self.tableView.resizeColumnsToContents()
        head = ["Name","#","Last Date","Last Msg"]
        for i in range(len(head)):
            self.tableView.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(head[i])) 

    def get_last_date(self, name):
        return "14/02/1992"

    def get_last_msg(self, name):
        return "Salut les poulets"

##############################################
##                  Code
##############################################
class Message:
	def __init__(self,listeInfo):
		self.date = listeInfo[0]
		self.heure = listeInfo[1]
		self.inout = listeInfo[2]
		self.numero = listeInfo[3]
		self.exp = listeInfo[4]
		self.message = listeInfo[5][:-1]
		
class Lecture:
	def __init__(self,fileName):
		fichier = open(fileName,'r')
		self.d = {}
		for lignes in fichier:
			liste = lignes.split('\t')
			mess = Message(liste)
			if mess.exp not in self.d.keys():
				self.d[mess.exp] = []
			self.d[mess.exp].append(mess)
	
##############################################
##                  Main
##############################################
if __name__ == "__main__":
    msgs = Lecture('back_20130303')
    
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow(msgs.d)
    mainwindow.show()
    sys.exit(app.exec_())

