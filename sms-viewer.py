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
    def __init__(self, listeInfo):
        self.dateheure = datetime.datetime.strptime(listeInfo[0]+' '+listeInfo[1], '%Y-%m-%d %H:%M:%S')
        self.inout = listeInfo[2]
        self.numero = listeInfo[3]
        self.exp = listeInfo[4]
        self.message = _fromUtf8(listeInfo[5][:-1])


##############################################
##                  GUI
##############################################
class ConvWindow(QtGui.QScrollArea):
    def __init__(self, name, msgs):
        self.msgs = msgs
        self.name = _fromUtf8(name)
        QtGui.QScrollArea.__init__(self)
        self.setWindowTitle("Conversation {}".format(self.name))
        self.gridLayout = QtGui.QGridLayout(self)
        # print self.msgs.keys()
        for num, msg in enumerate(self.msgs[name]):
            # print msg.message
            self.dispmsg(msg, num)

    def dispmsg(self, msg, num):
        self.lab = QtGui.QLabel()
        self.lab.setText(msg.message)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab.sizePolicy().hasHeightForWidth())
        self.lab.setSizePolicy(sizePolicy)
        self.lab.setMinimumSize(QtCore.QSize(0, 0))
        self.lab.setMaximumSize(QtCore.QSize(500, 16777215))
        self.lab.setWordWrap(True)
        if msg.inout == 'in':
            self.gridLayout.addWidget(self.lab, num, 0, 1, 3)
        elif msg.inout == 'out':
            self.lab.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
            self.gridLayout.addWidget(self.lab, num, 1, 1, 3)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        """ Show all conversations """
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle("Consultation SMS")
        self.resize(500, 600)

        self.centralwidget = QtGui.QWidget(self)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)

        self.verticalLayout = QtGui.QVBoxLayout()

        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)

        self.gridoftable = QtGui.QGridLayout(self.scrollArea)

        self.tableView = QtGui.QTableWidget(self.scrollArea)
        self.lecture('back_20130303')
        self.settable()

        self.tableView.itemDoubleClicked.connect(self.openconv)

        self.gridoftable.addWidget(self.tableView, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.scrollArea)

        self.pushButton = QtGui.QPushButton("Ok Go !", self.centralwidget)
        self.pushButton.released.connect(self.openconv)
        self.verticalLayout.addWidget(self.pushButton)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.marandspa([self.gridLayout, self.gridoftable, self.verticalLayout])

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.openconv()

    def marandspa(self, layouts):
        for layout in layouts:
            layout.setMargin(0)
            layout.setSpacing(0)

    def settable(self):
        """ All setters for the table """
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setStretchLastSection(True)  # Bord collant à la fenetre

        self.filltable()
        self.setheadertable()

        self.tableView.verticalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents)
        self.tableView.verticalHeader().setDefaultSectionSize(40)  # Hauteur des lignes
        self.tableView.resizeColumnToContents(0)  # Redimenssionne automatiquement la première colonne

    def openconv(self):
        name = self.tableView.item(self.tableView.currentRow(), 0).text().split('\n')[0]
        self.conv = ConvWindow(str(name), self.msgs)
        self.conv.show()

    def filltable(self):
        """ Fill the table with the list created by self.conversations() """
        self.conversations()

        self.tableView.setRowCount(len(self.conv))
        self.tableView.setColumnCount(len(self.conv[0]))

        for i, row in enumerate(self.conv):
            for j, col in enumerate(row):
                item = QtGui.QTableWidgetItem()
                item.setData(QtCore.Qt.EditRole, col)
                self.tableView.setItem(i, j, item)

    def setheadertable(self):
        """  Create columns headers """
        head = ["Name", "Last"]  # 2 columns (à mettre ailleurs / differement)
        for i in range(len(head)):
            self.tableView.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(head[i]))

    def lecture(self, fileName):
        """ Create self.msgs a dictionnary {names:[<Message object>]} """
        fichier = open(fileName, 'r')
        self.msgs = {}
        for lignes in fichier:
            items = lignes.split('\t')
            msg = Message(items)
            if msg.exp not in self.msgs.keys():
                self.msgs[msg.exp] = []
            self.msgs[msg.exp].append(msg)

    def conversations(self):
        """ Create self.conv a list of last msgs by names [name (#), last date & msg ] """
        self.conv = []
        for name in self.msgs.keys():
            try:
                int(name.split(';')[0])
            except ValueError:
                self.conv.append([_fromUtf8(name) + '\n({})'.format(str(len(self.msgs[name]))), self.get_last_date(self.msgs[name]) + '\n' + self.get_last_msg(self.msgs[name])])

    def get_last_date(self, name_msgs):
        return _fromUtf8(sorted(map(lambda x: x.dateheure.strftime('%Y-%m-%d %H:%M'), name_msgs))[-1])

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
