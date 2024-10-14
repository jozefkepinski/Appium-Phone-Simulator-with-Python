import threading
from tkinter import filedialog, Tk
import os
import glob
# Appium imports
from appium.webdriver.common.appiumby import AppiumBy
import json
import time

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


def load_list_values_from_json():
    """
    Loads the json file and adds all "test_case" to the list
    """
    r = Tk()
    r.withdraw()
    # Clear list before new assignment
    commands_line.clear()
    json_file = filedialog.askopenfilename(title="Select JSON file", filetypes=(("Json files", "*.json"),
                                                                                ("all files", "*.*")))
    try:
        if json_file:
            with open(json_file, 'r') as file:
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
        print("REC set to OFF")
        print(f"Recording: {record_flag}")
    else:
        record_flag = True
        print("REC set to ON")
        print(f"Recording: {record_flag}")
    return record_flag


def get_commands_line():
    """This is temporary function to read currently saved STEPS."""

    print(commands_line)


def store_testcase():
    """This function will save the current step sequence into a new created file (with "Running.py" name) """
    savefile = filedialog.asksaveasfilename(filetypes=[("TestCase", "*.py"), ("JSON Campaign", "*.json"),
                                                       ("all files", "*.*")], defaultextension=".py",
                                            initialdir='/')
    newfile = open(savefile, 'w')
    newfile.write(str(commands_line))
    newfile.close()
    print(f"File saved: {savefile}")


def open_report():
    """This function will OPEN the test case sequence as a read_file or newfile[0] variable """
    fileopen = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=[("TestCase", "*.py"), ("all files", "*.*")])
    print("Opened file", fileopen)
    read_file = open(fileopen, "r")
    global commands_line
    new_list = (list(read_file))
    commands_line = new_list[0]
    print(f"Loaded new list COMPLETED : \n {commands_line}")


class Functions:
    """Contain functions to run with appium driver."""

    def __init__(self, driver):
        self._driver = driver

    def start_new_campaign_thread(self):
        """It wraps a campaign in new thread."""
        thread = threading.Thread(target=self.run_json_campaign)
        thread.start()

    def start_new_tc_thread(self):
        """It wraps a test case in new thread."""
        thread = threading.Thread(target=self.execute_json_test_case)
        thread.start()

    def start_new_run_start_thread(self):
        """It wraps a test case in new thread."""
        if not record_flag:
            thread = threading.Thread(target=self.running_button)
            thread.start()
        else:
            print(f"Record is currently active and flag is set to:{record_flag}")
            print("Please uncheck the REC button to execute sequence.")

    def run_json_campaign(self):
        """It opens a file in Json format and execute test cases in campaign."""
        r = Tk()
        r.withdraw()
        json_file = filedialog.askopenfilename(title="Select file", filetypes=[("Json files", "*.json")])
        print(f"Executing Scenario file: {json_file}")

        if json_file:
            with open(json_file, 'r') as file:
                date = json.load(file)
                for campaign, test_cases in date["campaigns"].items():
                    print(f"Campaign: {campaign}")
                    for test_case, steps in test_cases["test_cases"].items():
                        print(f"Test Case: {test_case}")
                        for step_id in steps:
                            print(f"Step_id: {step_id['step_id']}")
                            print(f"Test Step execution: {step_id['test_step']}")
                            try:
                                if hasattr(self, step_id['test_step']):
                                    name_to_call = getattr(self, step_id['test_step'])
                                    name_to_call()
                                    time.sleep(1)
                                else:
                                    print(f"Fail: {step_id['test_step']} is not correct")
                            except AttributeError as e:
                                print(f"Fail {step_id['test_step']} and error {e}")
                    print(f"Campaign {campaign} executed successful.")

    def execute_json_test_case(self):
        """It opens a file in Json format and calls saved functions.
        """
        r = Tk()
        r.withdraw()
        json_file = filedialog.askopenfilename(title="Select file", filetypes=[("Json files", "*.json")])
        print(f"Executing Scenario file: {json_file}")
        try:
            if json_file:
                with open(json_file, 'r') as file:
                    date = json.load(file)

                test_cases = date.get("test cases", [])

                for case in test_cases:
                    name = case.get("test_step")
                    print(f"Trying to execute: {name}")
                    try:
                        if hasattr(self, name):
                            name_to_call = getattr(self, name)
                            name_to_call()
                            time.sleep(1)
                        else:
                            print(f'Fail: {name} is not correct')
                    except AttributeError as e:
                        print(f"Fail {name} and error {e}")
            else:
                print("No file selected")
        except Exception as e:
            print(f"Error occurred: {e}")

    def running_button(self):
        """The method takes a list and performs the functionalities contained is list."""
        for case in commands_line:
            if case in dir(self):
                name_to_call = getattr(self, case)
                name_to_call()
                time.sleep(1)
            else:
                print("Something went wrong")


    def press_home(self):
        """Go HOME screen"""
        print("Pressed home")
        self._driver.press_keycode(3)
        if record_flag:
            commands_line.append('press_home')

    def open_calendar(self):
        """Open Calendar"""
        print("Pressed open calendar")
        self._driver.press_keycode(208)
        if record_flag:
            commands_line.append('open_calendar')

    def open_contacts(self):
        """Open contacts"""
        print("Pressed open contacts")
        self._driver.press_keycode(207)
        if record_flag:
            commands_line.append('open_contacts')

    def open_settings(self):
        """Open settings"""
        print("Pressed open settings")
        self._driver.press_keycode(176)
        if record_flag:
            commands_line.append('open_settings')

    def press_action_up(self):
        """Press UP"""
        print("Pressed up")
        self._driver.press_keycode(1)
        if record_flag:
            commands_line.append('press_action_up')

    def press_action_down(self):
        """Press DOWN"""
        print("Pressed down")
        self._driver.press_keycode(0)
        if record_flag:
            commands_line.append('press_action_down')

    def press_enter(self):
        """Press ENTER"""
        print("Pressed enter")
        self._driver.press_keycode(66)
        if record_flag:
            commands_line.append('press_enter')

    def press_escape(self):
        """Press ESCAPE"""
        print("Pressed escape")
        self._driver.press_keycode(111)
        if record_flag:
            commands_line.append('press_escape')

    def press_cancel(self):
        """Press Cancel"""
        print("Pressed cancel")
        self._driver.press_keycode(2)
        if record_flag:
            commands_line.append('press_cancel')

    def press_back(self):
        """Press BACK"""
        print("Pressed back")
        self._driver.press_keycode(4)
        if record_flag:
            commands_line.append('press_back')

    def press_long_press(self):
        """Long Press"""
        print("Pressed long press")
        self._driver.press_keycode(128)
        if record_flag:
            commands_line.append('press_long_press')

    def open_soft_keyboard(self):
        """Open soft-keyboard"""
        print("Pressed open soft keyboard")
        self._driver.press_keycode(32)
        if record_flag:
            commands_line.append('open_soft_keyboard')

    def end_session_down(self):
        """End connection session"""
        print("Pressed end connection session")
        self._driver.quit()

    def press_switch_app(self):
        """Switch apps"""
        print("Pressed switch app")
        self._driver.press_keycode(187)
        if record_flag:
            commands_line.append('press_switch_app')

    def scroll_down(self):
        """Scroll down"""
        print("Scrolled down")
        self._driver.press_keycode(26)
        if record_flag:
            commands_line.append('scroll_down')

    def volume_up(self):
        """Press Volume UP"""
        print("Pressed Volume UP")
        self._driver.press_keycode(24)
        if record_flag:
            commands_line.append('volume_up')

    def volume_down(self):
        """Press Volume DOWN"""
        print("Pressed Volume DOWN")
        self._driver.press_keycode(25)
        if record_flag:
            commands_line.append('volume_down')

    def volume_mute(self):
        """Press MUTE"""
        print("Pressed MUTE")
        self._driver.press_keycode(164)
        if record_flag:
            commands_line.append('volume_mute')

    def press_menu(self):
        """Press MENU"""
        print("Pressed MENU")
        self._driver.press_keycode(82)
        if record_flag:
            commands_line.append('press_menu')

    def msg_main(self):
        """Go to Messages"""
        print("Went to Messages")
        self._driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Messages').click()
        self._driver.implicitly_wait(2)
        if record_flag:
            commands_line.append('msg_main')

    def msg_first_conv(self):
        """Go to first conversation on the list"""
        print("Went to first conversation on the list")
        self._driver.find_element(by=AppiumBy.ID, value='com.google.android.apps.messaging:id'
                                                        '/conversation_name').click()
        if record_flag:
            commands_line.append('msg_first_conv')

    def msg_read_txt(self):
        """Reads last text message"""
        print("Read last text message")
        read_text = self._driver.find_element(by=AppiumBy.ID, value='com.google.android.apps.messaging:id/message_text')
        text = read_text.text
        print(text)
        if record_flag:
            commands_line.append('msg_read_txt')

    def swipe_up(self):
        """Swipe up"""
        print("Swiped up")
        self._driver.swipe(150, 2000, 150, 1300, 1000)
        self._driver.implicitly_wait(2)
        if record_flag:
            commands_line.append('swipe_up')

    def open_files(self):
        """Open files"""
        print("Opened files")
        self._driver.find_element(by=AppiumBy.XPATH,
                                  value='//android.widget.TextView[@content-desc="Files"]').click()
        self._driver.implicitly_wait(2)
        if record_flag:
            commands_line.append('open_files')

    def timer(self):
        """Timer"""
        print("Got Timer")
        self._driver.set_page_load_timeout(5000)
        self._driver.timeouts(5000)

    def run_first_file(self):
        """Run first file"""
        print("Ran first file")
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
        print(contact_name)
        # Search contact
        for i in contact_name:
            print(i.text)
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

    "___________________________________________________________________________________________\
    _______________________________________END_________________________________________________"
