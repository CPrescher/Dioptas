# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created: Thu Jun  5 23:17:22 2014
# by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_mainView(object):
    def setupUi(self, mainView):
        mainView.setObjectName(_fromUtf8("mainView"))
        mainView.resize(1063, 669)
        mainView.setStyleSheet(_fromUtf8("#mainView, #calibration_tab, #mask_tab, #integration_tab {  \n"
                                         "     background: #3C3C3C;      \n"
                                         "    border: 5px solid #3C3C3C;\n"
                                         " }  \n"
                                         "\n"
                                         "QTabWidget::tab-bar{ \n"
                                         "    alignment: center;\n"
                                         "}\n"
                                         "\n"
                                         "QWidget{\n"
                                         "    color: #F1F1F1;\n"
                                         "}\n"
                                         "\n"
                                         "\n"
                                         "QTabBar::tab:left, QTabBar::tab:right {  \n"
                                         "     background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #3C3C3C, stop:1 #505050);\n"
                                         "     border: 1px solid  #5B5B5B;  \n"
                                         "    font: normal 14px;\n"
                                         "    color: #F1F1F1;\n"
                                         "     border-radius:2px;\n"
                                         "    \n"
                                         "    padding: 0px;\n"
                                         "     width: 20px;  \n"
                                         "    min-height:140px;\n"
                                         " }  \n"
                                         "\n"
                                         "\n"
                                         "QTabBar::tab::top, QTabBar::tab::bottom {  \n"
                                         "     background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #3C3C3C, stop:1 #505050);\n"
                                         "     border: 1px solid  #5B5B5B;  \n"
                                         "    border-right: 0px solid white;\n"
                                         "      color: #F1F1F1; \n"
                                         "    font: normal 11px;\n"
                                         "     border-radius:2px;\n"
                                         "     min-width: 80px;  \n"
                                         "    height: 19px;\n"
                                         "    padding: 0px;\n"
                                         "     margin-top: 1px ;\n"
                                         "    margin-right: 1px;\n"
                                         " }  \n"
                                         "QTabBar::tab::left:last, QTabBar::tab::right:last{\n"
                                         "    border-bottom-left-radius: 10px;\n"
                                         "    border-bottom-right-radius: 10px;\n"
                                         "}\n"
                                         "QTabBar::tab:left:first, QTabBar::tab:right:first{\n"
                                         "    border-top-left-radius: 10px;\n"
                                         "    border-top-right-radius: 10px;\n"
                                         "}\n"
                                         "\n"
                                         "QTabWidget, QTabWidget::tab-bar,  QTabWidget::panel, QWidget{  \n"
                                         "     background: #3C3C3C;      \n"
                                         " }  \n"
                                         "\n"
                                         "QTabWidget::tab-bar {\n"
                                         "    alignment: center;\n"
                                         "}\n"
                                         "\n"
                                         " QTabBar::tab:hover {  \n"
                                         "     border: 1px solid #ADADAD;  \n"
                                         " }  \n"
                                         "   \n"
                                         " QTabBar:tab:selected{  \n"
                                         "\n"
                                         "    background: qlineargradient(\n"
                                         "        x1: 0, y1: 1, \n"
                                         "        x2: 0, y2: 0,\n"
                                         "        stop: 0 #727272, \n"
                                         "        stop: 1 #444444\n"
                                         "    );\n"
                                         "     border:1px solid  #ADADAD;  \n"
                                         "}\n"
                                         "\n"
                                         "QTabBar::tab:bottom:last, QTabBar::tab:top:last{\n"
                                         "    border-top-right-radius: 10px;\n"
                                         "    border-bottom-right-radius: 10px;\n"
                                         "}\n"
                                         "QTabBar::tab:bottom:first, QTabBar::tab:top:first{\n"
                                         "    border-top-left-radius: 10px;\n"
                                         "    border-bottom-left-radius: 10px;\n"
                                         "}\n"
                                         " QTabBar::tab:top:!selected {  \n"
                                         "    margin-top: 1px;\n"
                                         "    padding-top:1px;\n"
                                         " }  \n"
                                         "QTabBar::tab:bottom:!selected{\n"
                                         "    margin-bottom: 1px;\n"
                                         "    padding-bottom:1px;\n"
                                         "}\n"
                                         "\n"
                                         "QGraphicsView {\n"
                                         "    border-style: none;\n"
                                         "}\n"
                                         "\n"
                                         " QLabel , QCheckBox, QGroupBox, QRadioButton, QListWidget::item, QPushButton, QToolBox::tab, QSpinBox, QDoubleSpinBox , QComboBox{  \n"
                                         "     color: #F1F1F1; \n"
                                         "    font-size: 12px;\n"
                                         " }  \n"
                                         " QCheckBox{  \n"
                                         "     border-radius: 5px;  \n"
                                         " }  \n"
                                         " QRadioButton, QCheckBox {  \n"
                                         "     font-weight: normal;  \n"
                                         "    height: 15px;\n"
                                         " }  \n"
                                         " \n"
                                         " QLineEdit  {  \n"
                                         "     border-radius: 2px;  \n"
                                         "     background: #F1F1F1;  \n"
                                         "     color: black;  \n"
                                         "    height: 18 px;\n"
                                         " }  \n"
                                         "\n"
                                         "QLineEdit::focus{\n"
                                         "    border-style: none;\n"
                                         "     border-radius: 2px;  \n"
                                         "     background: #F1F1F1;  \n"
                                         "     color: black;  \n"
                                         "}\n"
                                         "QSpinBox, QDoubleSpinBox {\n"
                                         "    background-color:  #F1F1F1;    \n"
                                         "    color: black;\n"
                                         "    margin-left: -15px;\n"
                                         "    margin-right: -2px;\n"
                                         "    height: 30px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox:!editable {\n"
                                         "    margin-left: 1px;\n"
                                         "    padding-left: 10px;\n"
                                         "    height: 23px;\n"
                                         "    background-color: #3C3C3C;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::item{\n"
                                         "    background-color: #3C3C3C;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::item::selected {\n"
                                         "    background-color: #505050;\n"
                                         "}\n"
                                         "\n"
                                         " QComboBox QAbstractItemView {\n"
                                         "    color:  #F1F1F1;\n"
                                         " }\n"
                                         "/* Indicator will shine through the label text if you don\'t make it hidden. */\n"
                                         "QComboBox::indicator{\n"
                                         "    background-color:transparent;\n"
                                         "    selection-background-color:transparent;\n"
                                         "    color:transparent;\n"
                                         "    selection-color:transparent;\n"
                                         "}\n"
                                         "QToolBox::tab:QToolButton{\n"
                                         "    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #3C3C3C, stop:1 #505050);\n"
                                         "     border: 1px solid  #5B5B5B;  \n"
                                         "\n"
                                         "     border-radius:2px;\n"
                                         "     padding-right: 10px;  \n"
                                         "    \n"
                                         "      color: #F1F1F1; \n"
                                         "    font-size: 12px;\n"
                                         "    padding: 3px;\n"
                                         "}\n"
                                         "  \n"
                                         "QPushButton{  \n"
                                         "     background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop:1 #505050);\n"
                                         "     border: 1px solid #5B5B5B;\n"
                                         "     border-radius: 5px; \n"
                                         "     padding-left: 8px;\n"
                                         "height: 18px;\n"
                                         "    padding-right: 8px;   \n"
                                         " }  \n"
                                         "QPushButton:pressed{\n"
                                         "        margin-top: 2,px;\n"
                                         "        margin-left: 2px;\n"
                                         "}\n"
                                         "QPushButton::disabled{\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton::hover{  \n"
                                         "     border:1px solid #ADADAD;  \n"
                                         " }  \n"
                                         " \n"
                                         "\n"
                                         "QPushButton::checked{\n"
                                         "    background: qlineargradient(\n"
                                         "        x1: 0, y1: 1, \n"
                                         "        x2: 0, y2: 0,\n"
                                         "        stop: 0 #727272, \n"
                                         "        stop: 1 #444444\n"
                                         "    );\n"
                                         "     border:1px solid #ADADAD;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton::focus {\n"
                                         "    outline: None;\n"
                                         "}\n"
                                         " QGroupBox {  \n"
                                         "     border: 1px solid #ADADAD;  \n"
                                         "     border-radius: 4px;  \n"
                                         "     margin-top: 7px;  \n"
                                         "     padding: 0px  \n"
                                         " }  \n"
                                         " QGroupBox::title {  \n"
                                         "      subcontrol-origin: margin;  \n"
                                         "      left: 20px  \n"
                                         "  }\n"
                                         "\n"
                                         "QSplitter::handle:hover {\n"
                                         "    background: #3C3C3C;\n"
                                         " }\n"
                                         "\n"
                                         "\n"
                                         "QGraphicsView{\n"
                                         "    border-style: none;\n"
                                         "}\n"
                                         "\n"
                                         "\n"
                                         "\n"
                                         "#click_x_lbl, #click_y_lbl, #click_int_lbl, #click_azi_lbl, #click_d_lbl, #click_tth_lbl, #click_q_lbl {\n"
                                         "    color: #00DD00;\n"
                                         "}\n"
                                         ""))
        self.gridLayout = QtGui.QGridLayout(mainView)
        self.gridLayout.setMargin(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(mainView)
        self.tabWidget.setStyleSheet(_fromUtf8(""))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.calibration_tab = QtGui.QWidget()
        self.calibration_tab.setObjectName(_fromUtf8("calibration_tab"))
        self.tabWidget.addTab(self.calibration_tab, _fromUtf8(""))
        self.mask_tab = QtGui.QWidget()
        self.mask_tab.setObjectName(_fromUtf8("mask_tab"))
        self.tabWidget.addTab(self.mask_tab, _fromUtf8(""))
        self.integration_tab = QtGui.QWidget()
        self.integration_tab.setObjectName(_fromUtf8("integration_tab"))
        self.tabWidget.addTab(self.integration_tab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(mainView)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainView)

    def retranslateUi(self, mainView):
        mainView.setWindowTitle(_translate("mainView", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.calibration_tab),
                                  _translate("mainView", "Calibration", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mask_tab), _translate("mainView", "Mask", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.integration_tab),
                                  _translate("mainView", "Integration", None))

