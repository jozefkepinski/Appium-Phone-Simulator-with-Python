import threading
import os
import glob
# Appium imports
from appium.webdriver.common.appiumby import AppiumBy
import json
import time
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QHBoxLayout, QPushButton
import logging
import QT_GUI.Welcome as Welcome
from PyQt5 import QtGui
# Variables
filename = ""
txtfiles = []
EXCEL_FILE_NAME = "Archive/Campaign.xlsx"
EXCEL_SHEET_NAME = "Test Suite"
main_path = os.path.dirname(os.path.abspath(__file__))

# Record flag for record session recognition
record_flag = False
commands_line = []

'''
#############################
#    FUNCTION BLOCK
#############################
'''


def load_list_values_from_json(parent):
    """
    Loads the json file and adds all "test_case" to the list
    """
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    json_file = QFileDialog.getOpenFileName(parent, "Select JSON file", "", "Json files", options=options)
    #r.withdraw()
    # Clear list before new assignment
    commands_line.clear()

    try:
        if json_file:
            with open(json_file[0], 'r') as file:
                date = json.load(file)
            for item in date["test cases"]:
                test_case = ''.join(item['test_step'])
                commands_line.append(test_case)
            get_commands_line()
            return commands_line
    except Exception as e:
        print(f"Error occurred: {e}")


def file_name_verify(name):
    """Verify (and change if necessary) is name of file is valid and do not contain unwanted or illegal characters
    -name : input -> string name to verify if contains unwanted characters
    if so then illegal characters will be removed from input name and returned as corrected
    """
    valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    output = ''.join(c for c in name if c in valid_chars)
    return output


def file_list():
    """Creates a file list of .py files. """
    for file in glob.glob("*.py"):
        txtfiles.append(file)


def output_write(testfile, output):
    """Write a line of output_write to the file.

    :param testfile: name of the file where string text will be included
    :param output: string text to insert inside 'testfile' file
    """
    testfile.write(output + "\n")
    # testfile.close()
    print("Output generated: %s" % (str(output)))


def set_record_flag():
    """Function set record_flag to True while 'step recorder' was started"""
    global record_flag
    if record_flag:
        record_flag = False
        logging.info("REC set to OFF")
        logging.info(f"Recording: {record_flag}")
    else:
        record_flag = True
        logging.info("REC set to ON")
        logging.info(f"Recording: {record_flag}")
    return record_flag


def get_commands_line():
    """This is temporary function to read currently saved STEPS."""

    logging.info(commands_line)


# def store_testcase():
#     """This function will save the current step sequence into a new created file (with "Running.py" name) """
#     savefile = filedialog.asksaveasfilename(filetypes=[("TestCase", "*.py"), ("JSON Campaign", "*.json"),
#                                                        ("all files", "*.*")], defaultextension=".py",
#                                             initialdir='/')
#     newfile = open(savefile, 'w')
#     newfile.write(str(commands_line))
#     newfile.close()
#     print(f"File saved: {savefile}")


# def open_report():
#     """This function will OPEN the test case sequence as a read_file or newfile[0] variable """
#     fileopen = filedialog.askopenfilename(initialdir="/", title="Select file",
#                                           filetypes=[("TestCase", "*.py"), ("all files", "*.*")])
#     print("Opened file", fileopen)
#     read_file = open(fileopen, "r")
#     global commands_line
#     new_list = (list(read_file))
#     commands_line = new_list[0]
#     print(f"Loaded new list COMPLETED : \n {commands_line}")


class Functions:
    """Contain functions to run with appium driver."""

    def __init__(self, driver):
        self._driver = driver

    def start_new_campaign_thread(self, qt_widget):
        """It wraps a campaign in new thread."""
        thread = threading.Thread(target=self.run_json_campaign(qt_widget))
        thread.start()

    def start_new_tc_thread(self, qt_widget):
        """It wraps a test case in new thread."""
        thread = threading.Thread(target=self.execute_json_test_case(qt_widget))
        thread.start()

    def start_new_run_start_thread(self):
        """It wraps a test case in new thread."""
        if not record_flag:
            thread = threading.Thread(target=self.running_button())
            thread.start()
        else:
            logging.info(f"Record is currently active and flag is set to:{record_flag}")
            logging.info("Please uncheck the REC button to execute sequence.")

    def run_json_campaign(self, qt_widget):
        """It opens a file in Json format and execute test cases in campaign."""
        qt_gui = QFileDialog()
        json_file, filter = qt_gui.getOpenFileName(parent=qt_widget, caption="Select campaign file", directory=".",
                                                   filter="Json files (*.json)")
        logging.info(f"Executing Scenario file: {json_file}")

        if json_file:
            with open(json_file, 'r') as file:
                date = json.load(file)
                for campaign, test_cases in date["campaigns"].items():
                    logging.info(f"Campaign: {campaign}")
                    for test_case, steps in test_cases["test_cases"].items():
                        logging.info(f"Test Case: {test_case}")
                        for step_id in steps:
                            logging.info(f"Step_id: {step_id['step_id']}")
                            logging.info(f"Test Step execution: {step_id['test_step']}")
                            try:
                                if hasattr(self, step_id['test_step']):
                                    name_to_call = getattr(self, step_id['test_step'])
                                    name_to_call()
                                    time.sleep(1)
                                else:
                                    logging.error(f"Fail: {step_id['test_step']} is not correct")
                            except AttributeError as e:
                                logging.error(f"Fail {step_id['test_step']} and error {e}")
                    logging.info(f"Campaign {campaign} executed successful.")

    def execute_json_test_case(self, qt_widget):
        """It opens a file in Json format and calls saved functions."""
        qt_gui = QFileDialog()
        json_file, filter = qt_gui.getOpenFileName(parent=qt_widget, caption="Select test case file", directory=".",
                                                   filter="Json files (*.json)")
        logging.info(f"Executing Scenario file: {json_file}")
        try:
            if json_file:
                with open(json_file, 'r') as file:
                    date = json.load(file)

                test_cases = date.get("test cases", [])

                for case in test_cases:
                    name = case.get("test_step")
                    logging.info(f"Trying to execute: {name}")
                    try:
                        if hasattr(self, name):
                            name_to_call = getattr(self, name)
                            name_to_call()
                            time.sleep(1)
                        else:
                            logging.error(f'Fail: {name} is not correct')
                    except AttributeError as e:
                        logging.error(f"Fail {name} and error {e}")
            else:
                logging.info("No file selected")
        except Exception as e:
            logging.error(f"Error occurred: {e}")

    def running_button(self):
        """The method takes a list and performs the functionalities contained is list."""
        for case in commands_line:
            if case in dir(self):
                name_to_call = getattr(self, case)
                name_to_call()
                time.sleep(1)
            else:
                logging.info("Something went wrong")


    def press_home(self):
        """Go HOME screen"""
        logging.info("Pressed home")
        self._driver.press_keycode(3)
        if record_flag:
            commands_line.append('press_home')

    def open_calendar(self):
        """Open Calendar"""
        logging.info("Pressed open calendar")
        self._driver.press_keycode(208)
        if record_flag:
            commands_line.append('open_calendar')

    def open_contacts(self):
        """Open contacts"""
        logging.info("Pressed open contacts")
        self._driver.press_keycode(207)
        if record_flag:
            commands_line.append('open_contacts')

    def open_settings(self):
        """Open settings"""
        logging.info("Pressed open settings")
        self._driver.press_keycode(176)
        if record_flag:
            commands_line.append('open_settings')

    def press_action_up(self):
        """Press UP"""
        logging.info("Pressed up")
        self._driver.press_keycode(1)
        if record_flag:
            commands_line.append('press_action_up')

    def press_action_down(self):
        """Press DOWN"""
        logging.info("Pressed down")
        self._driver.press_keycode(0)
        if record_flag:
            commands_line.append('press_action_down')

    def press_action_left(self):
        """Press LEFT"""
        logging.info("Pressed left")
        self._driver.press_keycode(1)
        if record_flag:
            commands_line.append('press_action_left')

    def press_action_right(self):
        """Press RIGHT"""
        logging.info("Pressed right")
        self._driver.press_keycode(2)
        if record_flag:
            commands_line.append('press_action_right')

    def press_enter(self):
        """Press ENTER"""
        logging.info("Pressed enter")
        self._driver.press_keycode(66)
        if record_flag:
            commands_line.append('press_enter')

    def press_escape(self):
        """Press ESCAPE"""
        logging.info("Pressed escape")
        self._driver.press_keycode(111)
        if record_flag:
            commands_line.append('press_escape')

    def press_cancel(self):
        """Press Cancel"""
        logging.info("Pressed cancel")
        self._driver.press_keycode(2)
        if record_flag:
            commands_line.append('press_cancel')

    def press_back(self):
        """Press BACK"""
        logging.info("Pressed back")
        self._driver.press_keycode(4)
        if record_flag:
            commands_line.append('press_back')

    def press_long_press(self):
        """Long Press"""
        logging.info("Pressed long press")
        self._driver.press_keycode(128)
        if record_flag:
            commands_line.append('press_long_press')

    def open_soft_keyboard(self):
        """Open soft-keyboard"""
        logging.info("Pressed open soft keyboard")
        self._driver.press_keycode(32)
        if record_flag:
            commands_line.append('open_soft_keyboard')

    def end_session_down(self, second_window):
        """End connected Appium session"""

        # Popup message
        msg = QMessageBox()
        ret = msg.question(second_window, "Session termination", "Are you sure to terminate session?", msg.Yes | msg.Cancel)

        if ret == msg.Yes:
            logging.info("Pressed end connection session")
            self._driver.quit()
            second_window.window().close()
            self.welcome = Welcome.Ui_MainWindow()
            self.welcome.outside_init()

        else:
            msg.information(second_window, "Session termination", "Nothing Changed")


    def press_switch_app(self):
        """Switch apps"""
        logging.info("Pressed switch app")
        self._driver.press_keycode(187)
        if record_flag:
            commands_line.append('press_switch_app')

    def scroll_down(self):
        """Scroll down"""
        logging.info("Scrolled down")
        self._driver.press_keycode(26)
        if record_flag:
            commands_line.append('scroll_down')

    def volume_up(self):
        """Press Volume UP"""
        logging.info("Pressed Volume UP")
        self._driver.press_keycode(24)
        if record_flag:
            commands_line.append('volume_up')

    def volume_down(self):
        """Press Volume DOWN"""
        logging.info("Pressed Volume DOWN")
        self._driver.press_keycode(25)
        if record_flag:
            commands_line.append('volume_down')

    def volume_mute(self):
        """Press MUTE"""
        logging.info("Pressed MUTE")
        self._driver.press_keycode(164)
        if record_flag:
            commands_line.append('volume_mute')

    def press_menu(self):
        """Press MENU"""
        logging.info("Pressed MENU")
        self._driver.press_keycode(82)
        if record_flag:
            commands_line.append('press_menu')

    def press_dialpad_left(self):
        """Press DPAD_left"""
        logging.info("Pressed DPAD LEFT")
        self._driver.press_keycode(21)
        if record_flag:
            commands_line.append('press_DPAD_left')

    def press_dialpad_right(self):
        """Press DPAD_right"""
        logging.info("Pressed DPAD RIGHT")
        self._driver.press_keycode(22)
        if record_flag:
            commands_line.append('press_DPAD_right')

    def msg_main(self):
        """Go to Messages"""
        logging.info("Went to Messages")
        self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Messages').click()
        self._driver.implicitly_wait(2)
        if record_flag:
            commands_line.append('msg_main')

    def msg_first_conv(self):
        """Go to first conversation on the list"""
        logging.info("Went to first conversation on the list")
        self._driver.find_element(by=AppiumBy.ID, value='com.google.android.apps.messaging:id'
                                                        '/conversation_name').click()
        if record_flag:
            commands_line.append('msg_first_conv')

    def msg_read_txt(self):
        """Reads last text message"""
        logging.info("Read last text message")
        read_text = self._driver.find_element(by=AppiumBy.ID, value='com.google.android.apps.messaging:id/message_text')
        text = read_text.text
        logging.info(text)
        if record_flag:
            commands_line.append('msg_read_txt')

    def swipe_up(self):
        """Swipe up"""
        logging.info("Swiped up")
        self._driver.swipe(150, 2000, 150, 1300, 1000)
        self._driver.implicitly_wait(2)
        if record_flag:
            commands_line.append('swipe_up')

    def open_files(self):
        """Open files"""
        logging.info("Opened files")
        self._driver.find_element(by=AppiumBy.XPATH,
                                  value='//android.widget.TextView[@content-desc="Files"]').click()
        self._driver.implicitly_wait(2)
        if record_flag:
            commands_line.append('open_files')

    def timer(self):
        """Timer"""
        logging.info("Got Timer")
        self._driver.set_page_load_timeout(5000)
        self._driver.timeouts(5000)

    def run_first_file(self):
        """Run first file"""
        logging.info("Ran first file")
        self._driver.find_element(by=AppiumBy.XPATH,
                                  value='/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout'
                                        '/android.widget.FrameLayout/android.widget.FrameLayout/android'
                                        '.widget.FrameLayout/android.view.ViewGroup/androidx.drawerlayout'
                                        '.widget.DrawerLayout/android.widget.ScrollView/android.widget'
                                        '.FrameLayout/android.widget.FrameLayout['
                                        '2]/android.widget.LinearLayout/android.view.ViewGroup/androidx'
                                        '.recyclerview.widget.RecyclerView/androidx.cardview.widget'
                                        '.CardView['
                                        '1]/androidx.cardview.widget.CardView/android.widget.RelativeLayout'
                                        '/android.widget.FrameLayout/android.widget.ImageView[1]').click()

    def test_dial_contact(self):
        """TestCase : Search for a specific contact, then dial a phone call -afterward call will be ended."""
        # Enter Home screen
        self._driver.press_keycode(3)
        # Find Home object and press it
        self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Home').click()
        # Find Phone object and press it
        self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Phone').click()
        # Wait
        self._driver.implicitly_wait(2)
        # Find element contact_name
        contact_name = self._driver.find_elements(by=AppiumBy.ID, value='com.google.android.dialer:id/contact_name')
        logging.info(contact_name)
        # Search contact
        for i in contact_name:
            logging.info(i.text)
        # Enter founded contact and press it
        self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Quick contact for Gruby').click()
        # Find Call object (icon) and press it
        self._driver.find_element(by=AppiumBy.ID, value='com.google.android.contacts:id/verb_call').click()

        self._driver.implicitly_wait(10)
        # Find End call object (icon) and press it
        self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='End call').click()
        # Go Home screen
        self._driver.press_keycode(3)
        # driver.quit()

    def create_contacts_pabloss(self):
        set_home = self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Home')
        set_home.click()
        # swipe up to open menu
        self._driver.swipe(150, 2000, 150, 1300, 1000)
        self._driver.implicitly_wait(2)
        open_contacts = self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Contacts')
        open_contacts.click()
        self._driver.implicitly_wait(2)
        create_contact = self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Create contact")
        self._driver.implicitly_wait(2)
        create_contact.click()
        self._driver.implicitly_wait(2)
        contact = self._driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text="First name"]')
        contact.send_keys("Pabloss")
        number = self._driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text="Phone"]')
        number.send_keys("434443443")
        self._driver.implicitly_wait(2)
        save = self._driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@text="Save"]')
        self._driver.implicitly_wait(2)
        save.click()
        self._driver.implicitly_wait(2)
        self._driver.press_keycode(3)

    def create_contacts_gruby(self):
        set_home = self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Home')
        set_home.click()
        # swipe up to open menu
        self._driver.swipe(150, 2000, 150, 1300, 1000)
        self._driver.implicitly_wait(2)
        open_contacts = self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Contacts')
        open_contacts.click()
        self._driver.implicitly_wait(2)
        create_contact = self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Create contact")
        self._driver.implicitly_wait(2)
        create_contact.click()
        self._driver.implicitly_wait(2)
        contact = self._driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text="First name"]')
        contact.send_keys("Gruby")
        number = self._driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text="Phone"]')
        number.send_keys("434466466")
        self._driver.implicitly_wait(2)
        save = self._driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@text="Save"]')
        self._driver.implicitly_wait(2)
        save.click()
        self._driver.implicitly_wait(2)
        self._driver.press_keycode(3)


    "___________________________________________________________________________________________\
    _______________________________________END_________________________________________________"
