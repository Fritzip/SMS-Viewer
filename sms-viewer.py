#! /bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


##############################################
##                  Message
##############################################

class Message:
	def __init__(self,listeInfo):
		self.dateheure = datetime.datetime.strptime(listeInfo[0]+' '+listeInfo[1], '%Y-%m-%d %H:%M:%S')
		self.inout = listeInfo[2]
		self.numero = listeInfo[3]
		self.exp = listeInfo[4]
		self.message = _fromUtf8(listeInfo[5][:-1])


##############################################
##                  GUI
##############################################

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
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
        self.lecture('back_20130303')
        self.settable()

        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.scrollArea)

        self.pushButton = QtGui.QPushButton("Ok Go !",self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        
        self.marandspa([self.gridLayout, self.gridLayout_2, self.verticalLayout])

    def marandspa(self,layouts):
        for layout in layouts:
            layout.setMargin(0)
            layout.setSpacing(0)
    
    def settable(self):
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.verticalHeader().setVisible(False)
        
        self.filltable()
        self.setheadertable()

        self.tableView.verticalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents);
        self.tableView.resizeColumnsToContents()


    def filltable(self):
        self.conversations()

        self.tableView.setRowCount(len(self.conv))
        self.tableView.setColumnCount(len(self.conv[0]))

        for i, row in enumerate(self.conv):
            for j, col in enumerate(row):
                item = QtGui.QTableWidgetItem()
                item.setData(QtCore.Qt.EditRole, col)
                self.tableView.setItem(i, j, item)
        
    def setheadertable(self):
        head = ["Name","#","Last Date","Last Msg"]
        for i in range(len(head)):
            self.tableView.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(head[i])) 
        
        
    def lecture(self, fileName):
        fichier = open(fileName,'r')
        self.msgs = {}
        for lignes in fichier:
            items = lignes.split('\t')
            msg = Message(items)
            if msg.exp not in self.msgs.keys():
                self.msgs[msg.exp] = []
            self.msgs[msg.exp].append(msg)

    def conversations(self):
        self.conv = []
        for name in self.msgs.keys():
            try:
                int(name.split(';')[0])
            except ValueError:
                self.conv.append([_fromUtf8(name),len(self.msgs[name]), self.get_last_date(self.msgs[name]), self.get_last_msg(self.msgs[name])])

    def get_last_date(self, name_msgs):
        return _fromUtf8(sorted(map(lambda x: x.dateheure.strftime('%Y-%m-%d %H:%M:%S'), name_msgs))[-1])
        
    def get_last_msg(self, name_msgs):
        return sorted(map(lambda x: x.message, name_msgs))[-1][:-1]

##############################################
##                  Main
##############################################
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

