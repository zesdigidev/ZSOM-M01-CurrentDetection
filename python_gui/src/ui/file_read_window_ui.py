# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'V3_ReadiraTWy.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(799, 750)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_13 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.Graph = QWidget(self.centralwidget)
        self.Graph.setObjectName(u"Graph")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Graph.sizePolicy().hasHeightForWidth())
        self.Graph.setSizePolicy(sizePolicy)
        self.Graph.setMinimumSize(QSize(780, 400))
        self.Graph.setStyleSheet(u"")

        self.verticalLayout_13.addWidget(self.Graph)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer_6 = QSpacerItem(148, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_6)

        self.ResetGraph_button_2 = QPushButton(self.centralwidget)
        self.ResetGraph_button_2.setObjectName(u"ResetGraph_button_2")

        self.horizontalLayout_12.addWidget(self.ResetGraph_button_2)


        self.verticalLayout_7.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.FileAttributes = QGroupBox(self.centralwidget)
        self.FileAttributes.setObjectName(u"FileAttributes")
        self.verticalLayout_3 = QVBoxLayout(self.FileAttributes)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Status_Label = QLabel(self.FileAttributes)
        self.Status_Label.setObjectName(u"Status_Label")

        self.horizontalLayout_3.addWidget(self.Status_Label)

        self.Stauts_Output = QLineEdit(self.FileAttributes)
        self.Stauts_Output.setObjectName(u"Stauts_Output")

        self.horizontalLayout_3.addWidget(self.Stauts_Output)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.FileSelect_Button = QPushButton(self.FileAttributes)
        self.FileSelect_Button.setObjectName(u"FileSelect_Button")

        self.horizontalLayout_2.addWidget(self.FileSelect_Button)

        self.Selected_file = QLineEdit(self.FileAttributes)
        self.Selected_file.setObjectName(u"Selected_file")

        self.horizontalLayout_2.addWidget(self.Selected_file)

        self.horizontalSpacer = QSpacerItem(128, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.horizontalLayout_13.addWidget(self.FileAttributes)


        self.verticalLayout_7.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_8 = QSpacerItem(78, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_8)

        self.ZESLOGO_2 = QWidget(self.centralwidget)
        self.ZESLOGO_2.setObjectName(u"ZESLOGO_2")
        self.ZESLOGO_2.setMinimumSize(QSize(191, 131))

        self.horizontalLayout_14.addWidget(self.ZESLOGO_2)

        self.horizontalSpacer_9 = QSpacerItem(98, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_9)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)


        self.horizontalLayout_11.addLayout(self.verticalLayout_7)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_11.addWidget(self.line_2)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.Graph_Attri_Box_2 = QGroupBox(self.centralwidget)
        self.Graph_Attri_Box_2.setObjectName(u"Graph_Attri_Box_2")
        self.verticalLayout = QVBoxLayout(self.Graph_Attri_Box_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TimestampBox_2 = QGroupBox(self.Graph_Attri_Box_2)
        self.TimestampBox_2.setObjectName(u"TimestampBox_2")
        self.gridLayout_3 = QGridLayout(self.TimestampBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.StartTime_Label_2 = QLabel(self.TimestampBox_2)
        self.StartTime_Label_2.setObjectName(u"StartTime_Label_2")

        self.gridLayout_3.addWidget(self.StartTime_Label_2, 0, 0, 1, 1)

        self.StartTime_Box_2 = QLineEdit(self.TimestampBox_2)
        self.StartTime_Box_2.setObjectName(u"StartTime_Box_2")
        self.StartTime_Box_2.setMinimumSize(QSize(0, 20))
        self.StartTime_Box_2.setMaximumSize(QSize(70, 16777215))
        self.StartTime_Box_2.setReadOnly(True)

        self.gridLayout_3.addWidget(self.StartTime_Box_2, 0, 1, 1, 1)

        self.EndTime_Label_2 = QLabel(self.TimestampBox_2)
        self.EndTime_Label_2.setObjectName(u"EndTime_Label_2")

        self.gridLayout_3.addWidget(self.EndTime_Label_2, 1, 0, 1, 1)

        self.EndTime_Box_2 = QLineEdit(self.TimestampBox_2)
        self.EndTime_Box_2.setObjectName(u"EndTime_Box_2")
        self.EndTime_Box_2.setMinimumSize(QSize(0, 20))
        self.EndTime_Box_2.setMaximumSize(QSize(70, 16777215))
        self.EndTime_Box_2.setReadOnly(True)

        self.gridLayout_3.addWidget(self.EndTime_Box_2, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.TimestampBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.AvgCurrentBox_2 = QGroupBox(self.Graph_Attri_Box_2)
        self.AvgCurrentBox_2.setObjectName(u"AvgCurrentBox_2")
        self.gridLayout_4 = QGridLayout(self.AvgCurrentBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.AverageCurrent_Box_2 = QLineEdit(self.AvgCurrentBox_2)
        self.AverageCurrent_Box_2.setObjectName(u"AverageCurrent_Box_2")
        self.AverageCurrent_Box_2.setMinimumSize(QSize(0, 20))
        self.AverageCurrent_Box_2.setMaximumSize(QSize(70, 16777215))
        self.AverageCurrent_Box_2.setReadOnly(True)

        self.gridLayout_4.addWidget(self.AverageCurrent_Box_2, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.AvgCurrentBox_2)

        self.SetPloted = QGroupBox(self.Graph_Attri_Box_2)
        self.SetPloted.setObjectName(u"SetPloted")
        self.gridLayout = QGridLayout(self.SetPloted)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit = QLineEdit(self.SetPloted)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 20))
        self.lineEdit.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.SetPloted)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_15.addWidget(self.Graph_Attri_Box_2)


        self.verticalLayout_8.addLayout(self.horizontalLayout_15)


        self.horizontalLayout_11.addLayout(self.verticalLayout_8)


        self.verticalLayout_13.addLayout(self.horizontalLayout_11)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.ResetGraph_button_2.setText(QCoreApplication.translate("MainWindow", u"Reset Graph", None))
        self.FileAttributes.setTitle(QCoreApplication.translate("MainWindow", u"File attributes", None))
        self.Status_Label.setText(QCoreApplication.translate("MainWindow", u"STATUS:", None))
        self.Stauts_Output.setText(QCoreApplication.translate("MainWindow", u"Status unknown", None))
        self.FileSelect_Button.setText(QCoreApplication.translate("MainWindow", u"File Select", None))
        self.Selected_file.setText(QCoreApplication.translate("MainWindow", u"Selected file", None))
        self.Graph_Attri_Box_2.setTitle(QCoreApplication.translate("MainWindow", u"Graph Attributes", None))
        self.TimestampBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp", None))
        self.StartTime_Label_2.setText(QCoreApplication.translate("MainWindow", u"Start Time:", None))
        self.StartTime_Box_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Start time", None))
        self.EndTime_Label_2.setText(QCoreApplication.translate("MainWindow", u"End Time:", None))
        self.EndTime_Box_2.setText("")
        self.EndTime_Box_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"End time", None))
        self.AvgCurrentBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Average Current", None))
        self.AverageCurrent_Box_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Average Current", None))
        self.SetPloted.setTitle(QCoreApplication.translate("MainWindow", u"Set ploted", None))
    # retranslateUi 