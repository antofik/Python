# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/database_settings.ui'
#
# Created: Sun Apr 21 22:52:31 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(336, 192)
        Dialog.setAutoFillBackground(False)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.LabelRole, self.formLayout)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.txtServer = QtGui.QLineEdit(self.groupBox)
        self.txtServer.setObjectName("txtServer")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtServer)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.txtPort = QtGui.QLineEdit(self.groupBox)
        self.txtPort.setObjectName("txtPort")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.txtPort)
        self.txtPassword = QtGui.QLineEdit(self.groupBox)
        self.txtPassword.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.txtPassword.setObjectName("txtPassword")
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.txtPassword)
        self.txtLogin = QtGui.QLineEdit(self.groupBox)
        self.txtLogin.setObjectName("txtLogin")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.txtLogin)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Database settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Параметры подключения к базе программы", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Сервер", None, QtGui.QApplication.UnicodeUTF8))
        self.txtServer.setText(QtGui.QApplication.translate("Dialog", "localhost", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Порт", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Логин", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Пароль", None, QtGui.QApplication.UnicodeUTF8))
        self.txtPort.setText(QtGui.QApplication.translate("Dialog", "3306", None, QtGui.QApplication.UnicodeUTF8))
        self.txtPassword.setText(QtGui.QApplication.translate("Dialog", "root", None, QtGui.QApplication.UnicodeUTF8))
        self.txtLogin.setText(QtGui.QApplication.translate("Dialog", "root", None, QtGui.QApplication.UnicodeUTF8))

