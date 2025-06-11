# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'V3_SerialmkLqdk.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(799, 832)
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
        self.Start_button_2 = QPushButton(self.centralwidget)
        self.Start_button_2.setObjectName(u"Start_button_2")

        self.horizontalLayout_12.addWidget(self.Start_button_2)

        self.Stop_button_2 = QPushButton(self.centralwidget)
        self.Stop_button_2.setObjectName(u"Stop_button_2")

        self.horizontalLayout_12.addWidget(self.Stop_button_2)

        self.horizontalSpacer_6 = QSpacerItem(148, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_6)

        self.ResetGraph_button_2 = QPushButton(self.centralwidget)
        self.ResetGraph_button_2.setObjectName(u"ResetGraph_button_2")

        self.horizontalLayout_12.addWidget(self.ResetGraph_button_2)


        self.verticalLayout_7.addLayout(self.horizontalLayout_12)

        self.Output_2 = QLineEdit(self.centralwidget)
        self.Output_2.setObjectName(u"Output_2")
        self.Output_2.setMinimumSize(QSize(321, 61))
        self.Output_2.setReadOnly(True)

        self.verticalLayout_7.addWidget(self.Output_2)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.Input_2 = QLineEdit(self.centralwidget)
        self.Input_2.setObjectName(u"Input_2")
        self.Input_2.setMinimumSize(QSize(321, 51))

        self.horizontalLayout_13.addWidget(self.Input_2)

        self.horizontalSpacer_7 = QSpacerItem(68, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_7)


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

        self.RecallFunctions_Box_2 = QGroupBox(self.centralwidget)
        self.RecallFunctions_Box_2.setObjectName(u"RecallFunctions_Box_2")
        self.verticalLayout_10 = QVBoxLayout(self.RecallFunctions_Box_2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.NormRecallBox_2 = QGroupBox(self.RecallFunctions_Box_2)
        self.NormRecallBox_2.setObjectName(u"NormRecallBox_2")
        self.horizontalLayout_16 = QHBoxLayout(self.NormRecallBox_2)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.NormalDataRecall_2 = QComboBox(self.NormRecallBox_2)
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.addItem("")
        self.NormalDataRecall_2.setObjectName(u"NormalDataRecall_2")

        self.horizontalLayout_16.addWidget(self.NormalDataRecall_2)

        self.Recall_Button_3 = QPushButton(self.NormRecallBox_2)
        self.Recall_Button_3.setObjectName(u"Recall_Button_3")

        self.horizontalLayout_16.addWidget(self.Recall_Button_3)


        self.verticalLayout_10.addWidget(self.NormRecallBox_2)

        self.AbRecallBox_2 = QGroupBox(self.RecallFunctions_Box_2)
        self.AbRecallBox_2.setObjectName(u"AbRecallBox_2")
        self.horizontalLayout_17 = QHBoxLayout(self.AbRecallBox_2)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.Abnormal_DataRecall_2 = QComboBox(self.AbRecallBox_2)
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.addItem("")
        self.Abnormal_DataRecall_2.setObjectName(u"Abnormal_DataRecall_2")

        self.horizontalLayout_17.addWidget(self.Abnormal_DataRecall_2)

        self.Recall_Button_4 = QPushButton(self.AbRecallBox_2)
        self.Recall_Button_4.setObjectName(u"Recall_Button_4")

        self.horizontalLayout_17.addWidget(self.Recall_Button_4)


        self.verticalLayout_10.addWidget(self.AbRecallBox_2)


        self.horizontalLayout_15.addWidget(self.RecallFunctions_Box_2)


        self.verticalLayout_8.addLayout(self.horizontalLayout_15)

        self.Storage_Status_Box_2 = QGroupBox(self.centralwidget)
        self.Storage_Status_Box_2.setObjectName(u"Storage_Status_Box_2")
        self.verticalLayout_11 = QVBoxLayout(self.Storage_Status_Box_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.NormalCapaticityBox_2 = QGroupBox(self.Storage_Status_Box_2)
        self.NormalCapaticityBox_2.setObjectName(u"NormalCapaticityBox_2")
        self.horizontalLayout_18 = QHBoxLayout(self.NormalCapaticityBox_2)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.Normal_Parti_storage_2 = QProgressBar(self.NormalCapaticityBox_2)
        self.Normal_Parti_storage_2.setObjectName(u"Normal_Parti_storage_2")
        self.Normal_Parti_storage_2.setValue(24)

        self.horizontalLayout_18.addWidget(self.Normal_Parti_storage_2)

        self.Norm_Clear_Button_2 = QPushButton(self.NormalCapaticityBox_2)
        self.Norm_Clear_Button_2.setObjectName(u"Norm_Clear_Button_2")

        self.horizontalLayout_18.addWidget(self.Norm_Clear_Button_2)


        self.verticalLayout_11.addWidget(self.NormalCapaticityBox_2)

        self.AbnormalCapaticityBox_2 = QGroupBox(self.Storage_Status_Box_2)
        self.AbnormalCapaticityBox_2.setObjectName(u"AbnormalCapaticityBox_2")
        self.verticalLayout_12 = QVBoxLayout(self.AbnormalCapaticityBox_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.Abnormal_Partition_Storage_2 = QProgressBar(self.AbnormalCapaticityBox_2)
        self.Abnormal_Partition_Storage_2.setObjectName(u"Abnormal_Partition_Storage_2")
        self.Abnormal_Partition_Storage_2.setValue(24)

        self.horizontalLayout_19.addWidget(self.Abnormal_Partition_Storage_2)

        self.Ab_Clear_Button_2 = QPushButton(self.AbnormalCapaticityBox_2)
        self.Ab_Clear_Button_2.setObjectName(u"Ab_Clear_Button_2")

        self.horizontalLayout_19.addWidget(self.Ab_Clear_Button_2)


        self.verticalLayout_12.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_11)

        self.AB_Auto_Clear_Checkbox_2 = QCheckBox(self.AbnormalCapaticityBox_2)
        self.AB_Auto_Clear_Checkbox_2.setObjectName(u"AB_Auto_Clear_Checkbox_2")

        self.horizontalLayout_20.addWidget(self.AB_Auto_Clear_Checkbox_2)


        self.verticalLayout_12.addLayout(self.horizontalLayout_20)


        self.verticalLayout_11.addWidget(self.AbnormalCapaticityBox_2)


        self.verticalLayout_8.addWidget(self.Storage_Status_Box_2)


        self.horizontalLayout_11.addLayout(self.verticalLayout_8)


        self.verticalLayout_13.addLayout(self.horizontalLayout_11)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Current Sense GUI V3 - Serial Read Mode [ Powered By ZSOM ]", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.Start_button_2.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.Stop_button_2.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.ResetGraph_button_2.setText(QCoreApplication.translate("MainWindow", u"Reset Graph", None))
        self.Output_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Output will appear here", None))
        self.Input_2.setText("")
        self.Input_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Input Here", None))
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
        self.RecallFunctions_Box_2.setTitle(QCoreApplication.translate("MainWindow", u"Recall Functions", None))
        self.NormRecallBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Normal Data Set Recall", None))
        self.NormalDataRecall_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Set 1", None))
        self.NormalDataRecall_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Set 2", None))
        self.NormalDataRecall_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Set 3", None))
        self.NormalDataRecall_2.setItemText(3, QCoreApplication.translate("MainWindow", u"Set 4", None))
        self.NormalDataRecall_2.setItemText(4, QCoreApplication.translate("MainWindow", u"Set 5", None))
        self.NormalDataRecall_2.setItemText(5, QCoreApplication.translate("MainWindow", u"Set 6", None))
        self.NormalDataRecall_2.setItemText(6, QCoreApplication.translate("MainWindow", u"Set 7", None))
        self.NormalDataRecall_2.setItemText(7, QCoreApplication.translate("MainWindow", u"Set 8", None))
        self.NormalDataRecall_2.setItemText(8, QCoreApplication.translate("MainWindow", u"Set 9", None))
        self.NormalDataRecall_2.setItemText(9, QCoreApplication.translate("MainWindow", u"Set 10", None))

        self.Recall_Button_3.setText(QCoreApplication.translate("MainWindow", u"Recall", None))
        self.AbRecallBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Abnormal Data Set Recall", None))
        self.Abnormal_DataRecall_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Set A1", None))
        self.Abnormal_DataRecall_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Set A2", None))
        self.Abnormal_DataRecall_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Set A3", None))
        self.Abnormal_DataRecall_2.setItemText(3, QCoreApplication.translate("MainWindow", u"Set A4", None))
        self.Abnormal_DataRecall_2.setItemText(4, QCoreApplication.translate("MainWindow", u"Set A5", None))
        self.Abnormal_DataRecall_2.setItemText(5, QCoreApplication.translate("MainWindow", u"Set A6", None))
        self.Abnormal_DataRecall_2.setItemText(6, QCoreApplication.translate("MainWindow", u"Set A7", None))
        self.Abnormal_DataRecall_2.setItemText(7, QCoreApplication.translate("MainWindow", u"Set A8", None))
        self.Abnormal_DataRecall_2.setItemText(8, QCoreApplication.translate("MainWindow", u"Set A9", None))
        self.Abnormal_DataRecall_2.setItemText(9, QCoreApplication.translate("MainWindow", u"Set A10", None))

        self.Recall_Button_4.setText(QCoreApplication.translate("MainWindow", u"Recall", None))
        self.Storage_Status_Box_2.setTitle(QCoreApplication.translate("MainWindow", u"FRAM STORAGE STATUS", None))
        self.NormalCapaticityBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Normal Partition Capaticy", None))
        self.Norm_Clear_Button_2.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.AbnormalCapaticityBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Abnormal Partition Capaticy", None))
        self.Ab_Clear_Button_2.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.AB_Auto_Clear_Checkbox_2.setText(QCoreApplication.translate("MainWindow", u"Auto Clear", None))
    # retranslateUi