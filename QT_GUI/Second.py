
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QInputDialog, QLineEdit
import Resources_QT
import logging
import Functions_QT
import Welcome
import os
import json
import driver_server
import pathlib
from datetime import datetime
from Functions_QT import commands_line


def exit_me():
    """Close the application."""
    print("Application closed successfully")
    exit()


class QTextEditLogger(logging.Handler, QtCore.QObject):
    """Logging area."""
    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QTextEdit(parent)
        self.widget.setGeometry(QtCore.QRect(10, 420, 781, 110))
        self.widget.setObjectName("Area_Logs")
        # Autoscroll to the bottom
        self.widget.y()

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)


class Ui_SecondWindow(object):
    """"""
    def __init__(self, driver_instance):
        self.device_id = None
        self.device_model = None
        self.driver = driver_server.Driver()
        self.driver_instance = driver_instance
        self.functions = Functions_QT.Functions
        # Load Config file
        self.main_path = os.getcwd()
        with open(f'{self.main_path}/../config/common.json') as config_file:
            self.data = json.load(config_file)
        self.rec_change_color = False
        self.selected_device = ""
        self.current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def setupUi(self, SecondWindow):
        # Main screen init
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Init Functions
        self.welcome = Welcome.Ui_MainWindow()
        create_driver, init_functions, self.selected_device = self.initialize_driver(self.driver_instance)

        if self.driver_instance.__name__ != "create_avd_driver":
            self.device_model = create_driver.capabilities["deviceModel"]
            self.device_id = create_driver.capabilities["deviceId"]
        else:
            self.device_model = create_driver.capabilities["avd"]
            self.device_id = create_driver.capabilities["deviceUDID"]

        def rec_button():
            """Change background color of Rec button and run handler function."""
            Functions_QT.set_record_flag()
            if self.rec_change_color:
                self.RecordButton.setStyleSheet("background-color: light gray")
                self.rec_change_color = False
            else:
                self.RecordButton.setStyleSheet("background-color: red")
                self.rec_change_color = True

        # Background init
        self.backgroundView = QtWidgets.QGraphicsView(self.centralwidget)
        self.backgroundView.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.backgroundView.setStyleSheet("background-image: url(:/Background/background_warm_APP.png)")
        self.backgroundView.setObjectName("backgroundView")
        # TOP Buttons setup
        self.DisconnectButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.end_session_down(self.centralwidget))
        self.DisconnectButton.setGeometry(QtCore.QRect(20, 10, 93, 28))
        self.DisconnectButton.setObjectName("DisconnectButton")
        self.RecordButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: rec_button())
        self.RecordButton.setGeometry(QtCore.QRect(350, 10, 93, 28))
        self.RecordButton.setObjectName("RecordButton")
        self.ClearLogsButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.clear_logs())
        self.ClearLogsButton.setGeometry(QtCore.QRect(560, 10, 93, 28))
        self.ClearLogsButton.setObjectName("ClearLogsButton")
        self.ExitButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: exit_me())
        self.ExitButton.setGeometry(QtCore.QRect(690, 10, 93, 28))
        self.ExitButton.setObjectName("ExitButton")
        self.RunTCButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda : init_functions.start_new_tc_thread(self.centralwidget))
        self.RunTCButton.setGeometry(QtCore.QRect(20, 50, 93, 28))
        self.RunTCButton.setObjectName("RunTCButton")
        self.RunCampButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda : init_functions.start_new_campaign_thread(self.centralwidget))
        self.RunCampButton.setGeometry(QtCore.QRect(120, 50, 93, 28))
        self.RunCampButton.setObjectName("RunCampButton")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget, clicked= init_functions.start_new_run_start_thread)
        self.StartButton.setGeometry(QtCore.QRect(300, 50, 93, 28))
        self.StartButton.setObjectName("StartButton")
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.show_save_window())
        self.SaveButton.setGeometry(QtCore.QRect(410, 50, 93, 28))
        self.SaveButton.setObjectName("SaveButton")
        # Device labels -connection info
        self.labelDevices = QtWidgets.QLabel(self.centralwidget)
        self.labelDevices.setGeometry(QtCore.QRect(30, 100, 111, 16))
        self.labelDevices.setObjectName("labelDevices")
        self.dev_ConnectonName_labelTEXT = QtWidgets.QLabel(self.centralwidget)
        self.dev_ConnectonName_labelTEXT.setGeometry(QtCore.QRect(150, 100, 111, 16))
        self.dev_ConnectonName_labelTEXT.setObjectName("dev_ConnectonName_labelTEXT")
        self.label_DevName = QtWidgets.QLabel(self.centralwidget)
        self.label_DevName.setGeometry(QtCore.QRect(30, 130, 111, 16))
        self.label_DevName.setObjectName("label_DevName")
        self.DevAddresslabel = QtWidgets.QLabel(self.centralwidget)
        self.DevAddresslabel.setGeometry(QtCore.QRect(30, 160, 111, 16))
        self.DevAddresslabel.setObjectName("DevAddresslabel")
        self.dev_Name_labelTEXT = QtWidgets.QLabel(self.centralwidget)
        self.dev_Name_labelTEXT.setGeometry(QtCore.QRect(150, 130, 111, 16))
        self.dev_Name_labelTEXT.setObjectName("dev_Name_labelTEXT")
        self.dev_Address_labelTEXT = QtWidgets.QLabel(self.centralwidget)
        self.dev_Address_labelTEXT.setGeometry(QtCore.QRect(150, 160, 111, 16))
        self.dev_Address_labelTEXT.setObjectName("dev_Address_labelTEXT")
        # BOTTOM buttons for actions
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.press_home())
        self.pushButton.setGeometry(QtCore.QRect(20, 230, 93, 28))
        self.pushButton.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.open_calendar())
        self.pushButton_2.setGeometry(QtCore.QRect(150, 230, 100, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.scroll_down())
        self.pushButton_3.setGeometry(QtCore.QRect(280, 230, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.volume_up())
        self.pushButton_4.setGeometry(QtCore.QRect(410, 230, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.volume_mute())
        self.pushButton_5.setGeometry(QtCore.QRect(540, 230, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.press_back())
        self.pushButton_6.setGeometry(QtCore.QRect(670, 230, 93, 28))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.volume_down())
        self.pushButton_7.setGeometry(QtCore.QRect(410, 280, 93, 28))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.open_contacts())
        self.pushButton_8.setGeometry(QtCore.QRect(150, 280, 93, 28))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.press_home())
        self.pushButton_9.setGeometry(QtCore.QRect(280, 280, 93, 28))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.press_action_up())
        self.pushButton_10.setGeometry(QtCore.QRect(540, 280, 93, 28))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.press_escape())
        self.pushButton_11.setGeometry(QtCore.QRect(20, 280, 93, 28))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.press_enter())
        self.pushButton_12.setGeometry(QtCore.QRect(670, 280, 93, 28))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.create_contacts_pabloss())
        self.pushButton_13.setGeometry(QtCore.QRect(280, 380, 93, 28))
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.press_action_left())
        self.pushButton_14.setGeometry(QtCore.QRect(410, 330, 93, 28))
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_15 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.open_settings())
        self.pushButton_15.setGeometry(QtCore.QRect(150, 330, 93, 28))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.press_menu())
        self.pushButton_16.setGeometry(QtCore.QRect(280, 330, 93, 28))
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_17 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.press_action_down())
        self.pushButton_17.setGeometry(QtCore.QRect(540, 330, 93, 28))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.open_soft_keyboard())
        self.pushButton_18.setGeometry(QtCore.QRect(20, 330, 93, 28))
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_19 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.press_long_press())
        self.pushButton_19.setGeometry(QtCore.QRect(150, 380, 93, 28))
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_20 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: init_functions.press_action_right())
        self.pushButton_20.setGeometry(QtCore.QRect(670, 330, 93, 28))
        self.pushButton_20.setObjectName("pushButton_20")
        self.pushButton_21 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.test_dial_contact())
        self.pushButton_21.setGeometry(QtCore.QRect(20, 380, 93, 28))
        self.pushButton_21.setObjectName("pushButton_21")
        self.pushButton_22 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.msg_main)
        self.pushButton_22.setGeometry(QtCore.QRect(670, 380, 93, 28))
        self.pushButton_22.setObjectName("pushButton_22")
        self.pushButton_23 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.msg_main)
        self.pushButton_23.setGeometry(QtCore.QRect(540, 380, 93, 28))
        self.pushButton_23.setObjectName("pushButton_23")
        self.pushButton_24 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: init_functions.create_contacts_gruby())
        self.pushButton_24.setGeometry(QtCore.QRect(410, 380, 93, 28))
        self.pushButton_24.setObjectName("pushButton_24")

        # log area (bottom)
        self.log_text_box = QTextEditLogger(self.centralwidget)
        # Save logs to file
        pathlib.Path(f'{self.main_path}\\Logs').mkdir(parents=True, exist_ok=True)
        logging.basicConfig(filename=f'{self.main_path}\\Logs\\Logs_{self.current_time}.log',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        # log to text box
        self.log_text_box.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(message)s'))
        logging.getLogger().addHandler(self.log_text_box)
        logging.getLogger().setLevel(logging.DEBUG)

        SecondWindow.setCentralWidget(self.centralwidget)
        # Menubar at the top of window
        self.menubar = QtWidgets.QMenuBar(SecondWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        SecondWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SecondWindow)
        self.statusbar.setObjectName("statusbar")
        SecondWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        # Naming
        SecondWindow.setWindowTitle(_translate("SecondWindow", "APPIUM Framework"))
        self.DisconnectButton.setText(_translate("SecondWindow", "Disconnect"))
        self.RecordButton.setText(_translate("SecondWindow", "Record"))
        self.ClearLogsButton.setText(_translate("SecondWindow", "Clear Logs"))
        self.ExitButton.setText(_translate("SecondWindow", "Exit"))
        self.RunTCButton.setText(_translate("SecondWindow", "Run TestCase"))
        self.RunCampButton.setText(_translate("SecondWindow", "Run Campaign"))
        self.StartButton.setText(_translate("SecondWindow", "Execute"))
        self.labelDevices.setText(_translate("SecondWindow", "Connected Device:"))
        self.dev_ConnectonName_labelTEXT.setText(_translate("SecondWindow", self.selected_device))
        self.label_DevName.setText(_translate("SecondWindow", "Device Name:"))
        self.DevAddresslabel.setText(_translate("SecondWindow", "Device Address:"))
        self.dev_Name_labelTEXT.setText(_translate("SecondWindow", self.device_model))
        self.dev_Address_labelTEXT.setText(_translate("SecondWindow", self.device_id))
        self.SaveButton.setText(_translate("SecondWindow", "SAVE"))
        self.pushButton.setText(_translate("SecondWindow", "Home button"))
        self.pushButton_2.setText(_translate("SecondWindow", "Calendar"))
        self.pushButton_3.setText(_translate("SecondWindow", "Scroll down"))
        self.pushButton_4.setText(_translate("SecondWindow", "Volume up"))
        self.pushButton_5.setText(_translate("SecondWindow", "Mute"))
        self.pushButton_6.setText(_translate("SecondWindow", "Back"))
        self.pushButton_7.setText(_translate("SecondWindow", "Volume Down"))
        self.pushButton_8.setText(_translate("SecondWindow", "Contacts"))
        self.pushButton_9.setText(_translate("SecondWindow", "Switch App"))
        self.pushButton_10.setText(_translate("SecondWindow", "Push Up"))
        self.pushButton_11.setText(_translate("SecondWindow", "ESCAPE"))
        self.pushButton_12.setText(_translate("SecondWindow", "ENTER"))
        self.pushButton_13.setText(_translate("SecondWindow", "Create Cont1"))
        self.pushButton_14.setText(_translate("SecondWindow", "Push Left"))
        self.pushButton_15.setText(_translate("SecondWindow", "Settings"))
        self.pushButton_16.setText(_translate("SecondWindow", "Press Menu"))
        self.pushButton_17.setText(_translate("SecondWindow", "Push Down"))
        self.pushButton_18.setText(_translate("SecondWindow", "SK Keyboard"))
        self.pushButton_19.setText(_translate("SecondWindow", "Long Press"))
        self.pushButton_20.setText(_translate("SecondWindow", "Push Right"))
        self.pushButton_21.setText(_translate("SecondWindow", "TC DialContact"))
        self.pushButton_22.setText(_translate("SecondWindow", "Cancel"))
        self.pushButton_23.setText(_translate("SecondWindow", "Messages"))
        self.pushButton_24.setText(_translate("SecondWindow", "Create Cont2"))
        self.menuFile.setTitle(_translate("SecondWindow", "File"))
        self.menuOptions.setTitle(_translate("SecondWindow", "Options"))

    def initialize_driver(self, init_driver):
        """Initialize driver."""
        if init_driver.__name__ == "create_wifi_driver":
            create_driver = self.driver.create_wifi_driver(
                {'newCommandTimeout': self.data["newCommandTimeout"], "deviceId": self.data["wifi"]["device_id"]})
            init_functions = self.functions(create_driver)
            selected_device = "WIFI"

        elif init_driver.__name__ == "create_usb_driver":
            create_driver = self.driver.create_usb_driver(
                {'newCommandTimeout': self.data["newCommandTimeout"], "deviceId": self.data["usb"]["device_id"]})
            init_functions = self.functions(create_driver)
            selected_device = "USB"

        else:
            create_driver = self.driver.create_avd_driver({'newCommandTimeout': self.data["newCommandTimeout"]})
            init_functions = self.functions(create_driver)
            selected_device = "AVD"
        return create_driver, init_functions, selected_device

    def setup_ui_save_window(self, save_window):
        save_window.setObjectName("SaveWindow")
        save_window.setWindowTitle("Save Options")
        # Create a QHBoxLayout instance
        layout = QHBoxLayout()
        # Add widgets to the layout
        save_tc_btn = QPushButton("Save_TC", clicked=lambda: self.save_tc_scenario(save_window))
        layout.addWidget(save_tc_btn)
        layout.addWidget(QPushButton("Save_Campaign", clicked=lambda: self.save_campaign(save_window)), 1)
        layout.addWidget(QPushButton("Cancel"), 2)
        # Set the layout on the application's window
        save_window.setLayout(layout)

    def show_save_window(self):
        """Window created for save TC and Campaign"""
        self.save_window = QtWidgets.QWidget()
        self.setup_ui_save_window(self.save_window)
        self.save_window.show()

    def save_tc_scenario(self, save_window):
        """It saves the file in JSON format."""
        try:
            file_name = f"test_case_{self.current_time}.json"

            folder = "TESTS"
            if not os.path.exists(folder):
                os.makedirs(folder)

            path = os.path.join(folder, file_name)

            test_cases = [{"step_id": index, "test_step": value} for index, value in enumerate(commands_line, 1)]
            date = {"test cases": test_cases}

            with open(path, 'w', encoding='utf-8') as file:
                json.dump(date, file, ensure_ascii=False, indent=4)
            save_window.close()
        except Exception as e:
            print(f"Error occurred: {e}")

    def save_campaign(self, save_window):
        """It saves the campaign file in JSON format."""
        try:
            campaign_name, camp_ok = QInputDialog.getText(save_window, 'Input', 'Enter campaign name:')
            test_case_name, tc_ok = QInputDialog.getText(save_window, 'Input', 'Enter test case name:')

            file_name = f"campaign_{self.current_time}.json"

            folder = "TESTS"
            if not os.path.exists(folder):
                os.makedirs(folder)

            path = os.path.join(folder, file_name)
            print(f"Scenario saved in root folder: {path}")

            test_cases = [{"step_id": index, "test_step": value} for index, value in enumerate(commands_line, 1)]
            date = test_cases

            with open(path, 'w', encoding='utf-8') as file:
                json.dump({"campaigns": {f"{campaign_name}": {"test_cases": {f"{test_case_name}": date}}}}, file,
                          ensure_ascii=False, indent=4)
            save_window.close()
        except Exception as e:
            print(f"Error occurred: {e}")

    def clear_logs(self):
        """Method for log area clearing."""
        self.log_text_box.widget.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SecondWindow = QtWidgets.QMainWindow()
    ui = Ui_SecondWindow(driver_server)
    ui.setupUi(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())
