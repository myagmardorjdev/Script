from PyQt5 import QtWidgets,QtCore

# Your existing Ui_MainWindow class definition

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.actionmission1.triggered.connect(self.openNewWindow)

    def openNewWindow(self):
        new_window = QtWidgets.QMainWindow()
        new_ui = Ui_NewWindow()
        new_ui.setupUi(new_window)
        new_window.show()

class Ui_NewWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("NewWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "New Window"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
