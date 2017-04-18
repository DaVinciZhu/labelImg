#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

class LoginDialog(QDialog):
    Signal_User = pyqtSignal(str)
    __username__ = 'Default'

    def __init__(self,parent = None):
        super(LoginDialog,self).__init__(parent)

        layout = QVBoxLayout()
        self.usr = QLineEdit(self)
        self.usr.setPlaceholderText(u'用户名')
        self.pbLogin = QPushButton(u'登录',self)
        # self.pbCancel = QPushButton(u'取消',self)

        self.pbLogin.clicked.connect(self.accept)
        # self.pbCancel.clicked.connect(self.reject)

        layout.addWidget(self.usr)
        layout.addWidget(self.pbLogin)
        self.setLayout(layout)
        # self.usr.selectAll()
        # self.usr.setFocus()
        self.setWindowTitle(u'登录界面')

        self.connect(self.pbLogin,SIGNAL('clicked()'),self,SLOT('myfunc()'))
        # self.connect(self.btn,SIGNAL('clicked()'),self.,SIGNAL(''))

    @pyqtSlot()
    def myfunc(self):
        # print 'self.usr.text()',self.usr.text()
        self.Signal_User.emit((self.usr.text()))


    # @staticmethod
    # def getUser(parent = None):
    #     usr = Login(parent)
    #     result = usr.exec_()
    #     data = usr.text()
    #     print 'data',data
    #     print result == QDialog.Accepted
    #     return (data,result == QDialog.Accepted)
