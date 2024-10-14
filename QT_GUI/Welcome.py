
from PyQt5 import QtCore, QtGui, QtWidgets
import Resources_QT
import Second
import driver_server

def exit_me():
    """Close the application."""
    print("Application closed successfully")
    exit()


class ComboBox(QtWidgets.QComboBox):
    # https://code.qt.io/cgit/qt/qtbase.git/tree/src/widgets/widgets/qcombobox.cpp?h=5.15.2#n3173
    def paintEvent(self, event):

        painter = QtWidgets.QStylePainter(self)
        painter.setPen(self.palette().color(QtGui.QPalette.Text))

        # draw the combobox frame, focusrect and selected etc.
        opt = QtWidgets.QStyleOptionComboBox()
        self.initStyleOption(opt)
        painter.drawComplexControl(QtWidgets.QStyle.ComplexControl.CC_ComboBox, opt)

        if self.currentIndex() < 0:
            opt.palette.setBrush(
                QtGui.QPalette.ButtonText,
                opt.palette.brush(QtGui.QPalette.ButtonText).color().lighter(),
            )
            if self.placeholderText():
                opt.currentText = self.placeholderText()

        # draw the icon and text
        painter.drawControl(QtWidgets.QStyle.ControlElement.CE_ComboBoxLabel, opt)


class Ui_MainWindow(object):

    def __init__(self):
        self.driver = driver_server.Driver()

    def openMainApp(self):
        """Main application init"""
        self.window = QtWidgets.QMainWindow()
        self.ui = Second.Ui_SecondWindow(self.new_driver)
        self.ui.setupUi(self.window)
        self.window.show()
        MainWindow.close()


    def setupUi(self, MainWindow):
        # Main screen init
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(795, 560)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Buttons
        self.Connect_bt = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.openMainApp())
        self.Connect_bt.setGeometry(QtCore.QRect(340, 110, 93, 28))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 241, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 241, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 241, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.Connect_bt.setPalette(palette)
        self.Connect_bt.setObjectName("Connect_bt")
        self.Connect_bt.setStyleSheet("background-color: #76EE00")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 220, 93, 28))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.pushButton.setPalette(palette)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("background-color: red")
        self.pushButton.clicked.connect(exit_me)
        # Menu combo-box
        self.comboBox = ComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(320, 160, 175, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("background-color: cornsilk")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setPlaceholderText("--Please select device--")
        self.comboBox.setCurrentIndex(-1)

        # Background image
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(-5, -9, 811, 571))
        self.graphicsView.setStyleSheet("background-image: url(:/Background/ACN_background_Welcome.png);")
        self.graphicsView.setObjectName("graphicsView")
        #Set all objects
        self.graphicsView.raise_()
        self.Connect_bt.raise_()
        self.pushButton.raise_()
        self.comboBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # Naming
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Connect_bt.setText(_translate("MainWindow", "CONNECT"))
        self.pushButton.setText(_translate("MainWindow", "Exit"))
        self.comboBox.setItemText(0, _translate("MainWindow", "AVD"))
        self.comboBox.setItemText(1, _translate("MainWindow", "USB"))
        self.comboBox.setItemText(2, _translate("MainWindow", "WIFI"))
        self.comboBox.activated[str].connect(self.change_driver)

        self.driver_options = {"AVD": self.driver.create_avd_driver, "USB": self.driver.create_usb_driver,
                               "WIFI": self.driver.create_wifi_driver}
        self.new_driver = self.driver

    def change_driver(self, options):
        """Method to select specific driver."""
        self.new_driver = self.driver_options[options]

    def outside_init(self):
        """Method to create main window outside."""
        global MainWindow
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
