"""
#######################################################################################################################
# Framework for APPIUM connectivity
# Project : Appium Phone Simulator with Python
# Authors: Pawel Grzesiuk, Ryszard Zajac, Jacek Kalis, Jozef Kepinski, Marcin Murawski
#######################################################################################################################
"""
import tkinter
import tkinter.scrolledtext as scrolled_text
import logging

import sys
from tkinter import *
from tkinter import messagebox as mess
from tkinter import Tk, simpledialog
import Functions

import driver_server
import os
from PIL import ImageTk, Image
import pathlib
import json

from datetime import datetime
from Functions import commands_line, load_list_values_from_json

# Variables :
main_path = os.getcwd()
authors = "- Grzesiuk Pawel\n" \
          "- Zajac Ryszard\n" \
          "- Kalis Jacek\n" \
          "- Kepinski Jozef\n" \
          "- Murawski Marcin"

# GUI handler
gui = Tk()


class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tkinter.END, msg + '\n')
            self.text.configure(state='normal')
            # Autoscroll to the bottom
            self.text.yview(tkinter.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


def gui_scalling(width, height, set_gui):
    """Function to set a generated window to center of the screen"""
    screen_width = gui.winfo_screenwidth()  # Width of the screen
    screen_height = gui.winfo_screenheight()  # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    set_gui.geometry('%dx%d+%d+%d' % (width, height, x, y))


# GUI creation
gui.title('APPIUM Pew-Ry-Ja [ver.NAiROBi]')
gui_scalling(width=800, height=600, set_gui=gui)
menu_top_frame = Frame(gui, bg='deepskyblue3', width=800)

# Image Data
img = ImageTk.PhotoImage(Image.open(main_path + "\\Resources\\Images\\PHONE_small.png"))
img_welcome_view = ImageTk.PhotoImage(Image.open(main_path + "\\Resources\\Images\\background_warm_APP.png"))

# Add text widget to display logging info
log_area = scrolled_text.ScrolledText(height=7, name="log_area", state='normal')
log_area.configure(font='TkFixedFont')

# Create textLogger
text_handler = TextHandler(log_area)

# Logging configuration
pathlib.Path(f'{main_path}\\Logs').mkdir(parents=True, exist_ok=True)
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logging.basicConfig(filename=f'{main_path}\\Logs\\Logs_{current_time}.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add the handler to logger
logger = logging.getLogger()
logger.addHandler(text_handler)

# Load Config file
with open('config/common.json') as config_file:
    data = json.load(config_file)

rec_change_color = False


def message_info(msg):
    """Show information in info box about processing."""
    mess.showinfo(title="Starting", message=msg)


def message_authors():
    """Show information about authors"""
    global authors
    mess.showinfo(title="Authors:", message=str(authors))


def clear_logs():
    """Clear logs."""
    log_area.delete(1.0, END)


class StdOutCatch:
    def write(self, txt):
        if "\n" not in txt:
            logger.info(txt)

    def flush(self):
        pass


def exit_now():
    """Close the application."""
    print("Application closed successfully")
    exit()


sys.stdout = StdOutCatch()


def driver_init(driver_instance):
    """Initialize android webdriver"""
    logger.info("Connecting driver...")
    device_id = "None"
    # Gain values of connected devices to display them on main app
    create_driver, init_functions = initialize_driver(driver_instance)
    device_model = create_driver.capabilities["deviceModel"]
    if "avd" not in create_driver.capabilities.keys():
        device_id = create_driver.capabilities["deviceId"]

    logger.info("Driver connected.")

    bt_connect.grid_forget()
    intro_center.grid_forget()
    # grid frames
    menu_top_frame.grid(row=0, sticky="nsew")
    center3 = Frame(gui, bg='aquamarine1')
    center3.grid(row=1, sticky="nsew")
    # logs window
    log_area.grid(row=3, sticky="s")

    ctr_up = Frame(center3, bg='darkslategray3')
    ctr_left = Frame(center3, bg='aquamarine1')
    ctr_right = Frame(center3, bg='aquamarine1')

    # grid 3 centers
    ctr_up.grid(row=0, column=0, sticky="nsew", ipadx=300)
    ctr_left.grid(row=1, column=0, sticky="NW", ipady=128, ipadx=80)
    ctr_right.grid(row=1, column=0, sticky="E", ipady=244, ipadx=72)

    def exit_0():
        """Close appium driver."""
        print("Appium driver was flushed successfully")
        create_driver.quit()
        exit()

    def create_buttons():
        """Window created for save TC and Campaign"""
        global window
        window = tkinter.Toplevel(bg='lightsteelblue3')
        gui_scalling(width=150, height=120, set_gui=window)

        save_button = tkinter.Button(window, text="SAVE TestCase", bg='lightsteelblue2',
                                     command=save_scenario, font=("Times New Roman", 11))
        save_button.grid(row=0, column=0, sticky="nsew", ipadx=10, pady=15, padx=12)

        save_button_campaign = tkinter.Button(window, text="SAVE Campaign",bg='lightsteelblue2',
                                              command=save_scenario_popup, font=("Times New Roman", 11))
        save_button_campaign.grid(row=1, column=0, sticky="nsew", ipadx=10, pady=10, padx=12)

    def save_scenario():
        """It saves the file in JSON format."""
        try:
            file_name = f"test_case_{current_time}.json"

            folder = "TESTS"
            if not os.path.exists(folder):
                os.makedirs(folder)

            path = os.path.join(folder, file_name)

            test_cases = [{"step_id": index, "test_step": value} for index, value in enumerate(commands_line, 1)]
            date = {"test cases": test_cases}

            with open(path, 'w', encoding='utf-8') as file:
                json.dump(date, file, ensure_ascii=False, indent=4)
            window.destroy()
        except Exception as e:
            print(f"Error occurred: {e}")

    def save_scenario_popup():
        """It saves the campaign file in JSON format."""
        try:
            root = Tk()
            root.withdraw()
            campaign_name = simpledialog.askstring("Input", "Enter campaign name:")
            test_case_name = simpledialog.askstring("Input", "Enter test case name:")

            file_name = f"campaign_{current_time}.json"

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
            window.destroy()
        except Exception as e:
            print(f"Error occurred: {e}")

    def disconnect_session():
        """Close appium session."""
        print("Appium session was flushed successfully")
        create_driver.quit()

    def rec_button():
        """Change background color of Rec button and run handler function."""
        global rec_change_color
        Functions.set_record_flag()
        if rec_change_color:
            bt_rec['bg'] = "seashell3"
            rec_change_color = False
        else:
            bt_rec['bg'] = "orangered1"
            rec_change_color = True

# BUTTONS configuration and display
    bt_disconnect = Button(menu_top_frame, text="DISCONNECT", command=disconnect_session, bg='#B7B7B7',
                           activebackground='orangered1')
    bt_disconnect.grid(row=0, column=0, padx=10, ipadx=17, pady=4, sticky="W")

    bt_clear_log = Button(menu_top_frame, text="ClearLog", command=clear_logs, bg='seashell3',
                          activebackground='orangered1')
    bt_clear_log.grid(row=0, column=1, padx=70, sticky="E")

    bt_rec = Button(menu_top_frame, text="REC", command=lambda:rec_button(), bg='seashell3')
    bt_rec.grid(row=0, column=2, padx=70, ipadx=17, pady=4)

    bt_exit1 = Button(menu_top_frame, text="Exit", command=exit_now, bg='#B7B7B7', activebackground='orangered1')
    bt_exit1.grid(row=0, column=3, padx=70, sticky="E")

    bt_load_scenario = Button(menu_top_frame, text="Run TC", command=init_functions.start_new_tc_thread,
                              bg='olivedrab2', activebackground='orangered1')
    bt_load_scenario.grid(row=1, column=0, padx=10, ipadx=1, pady=15, sticky="W")

    bt_run_start = Button(menu_top_frame, text="Run Campaign", command=init_functions.start_new_campaign_thread,
                          bg='olivedrab2', activebackground='orangered1')
    bt_run_start.grid(row=1, column=0, padx=65, pady=15, sticky="E")

    bt_run_start = Button(menu_top_frame, text="Run/Start", command=init_functions.start_new_run_start_thread,
                          bg='olivedrab2', activebackground='orangered1')
    bt_run_start.grid(row=1, column=1, padx=70, ipadx=1, pady=15, sticky="W")

    bt_save_scenario = Button(menu_top_frame, text="SAVE TC", command=create_buttons, bg='seashell2',
                              activebackground='orangered1')
    bt_save_scenario.grid(row=1, column=2, padx=75, pady=15, sticky="E")

    bt_disconnect = Button(menu_top_frame, text="Load TC Steps", command=load_list_values_from_json, bg='seashell3',
                           activebackground='orangered1')
    bt_disconnect.grid(row=1, column=3, padx=60, sticky="E")

    Label(ctr_up, text="Connected device:", bg="lightskyblue1").grid(row=0, column=0, padx=10, pady=10)
    Label(ctr_up, text="Device Name:", bg="darkseagreen2").grid(row=1, column=0, padx=10, pady=10)
    entry_sheet = Entry(ctr_up, background="orange")
    entry_sheet.grid(row=1, column=1)
    entry_sheet.insert(10, device_model)

    Label(ctr_up, text="Device Address:", bg="darkseagreen2").grid(row=2, column=0, padx=10, pady=10)
    entry_doc = Entry(ctr_up, background="orange")
    entry_doc.grid(row=2, column=1)
    if "avd" not in create_driver.capabilities.keys():
        entry_doc.insert(10, device_id)
    else:
        entry_doc.insert(10, "AVD")

    # Row 0 with label
    Label(ctr_left, text="Commands :", bg="darkslategray1").grid(row=0, column=0, ipadx=10, pady=10)

    # Row 1
    bt_press_home = Button(ctr_left, text="Press HOME", command=init_functions.press_home, bg='darkolivegreen1',
                           activebackground='orangered1')
    bt_press_home.grid(row=1, column=0, ipady=6, ipadx=7, padx=3, pady=5)

    bt_calendar = Button(ctr_left, text="Calendar", command=init_functions.open_calendar, bg='seashell1',
                         activebackground='orangered1')
    bt_calendar.grid(row=1, column=1, ipady=6, ipadx=7, padx=3, pady=5)

    bt_scroll_down = Button(ctr_left, text="Scroll Down", command=init_functions.scroll_down, bg='seashell1',
                            activebackground='orangered1')
    bt_scroll_down.grid(row=1, column=2, ipady=6, ipadx=7, padx=3, pady=5)

    bt_volume_up = Button(ctr_left, text="Volume Up", command=init_functions.volume_up, bg='darkseagreen2',
                          activebackground='orangered1')
    bt_volume_up.grid(row=1, column=3, ipady=6, ipadx=7, padx=3, pady=5)

    bt_press_mute = Button(ctr_left, text="Press Mute", command=init_functions.volume_mute, bg='darkseagreen1',
                           activebackground='orangered1')
    bt_press_mute.grid(row=1, column=4, ipady=6, ipadx=10, padx=3, pady=5)

    bt_press_back = Button(ctr_left, text="Press Back", command=init_functions.press_back, bg='darkolivegreen1',
                           activebackground='orangered1')
    bt_press_back.grid(row=1, column=5, ipady=6, ipadx=7, padx=3, pady=5)

    # Row 2
    bt_switch_app = Button(ctr_left, text="Switch App", command=init_functions.press_switch_app, bg='seashell1',
                           activebackground='orangered1')
    bt_switch_app.grid(row=2, column=0, ipady=6, ipadx=7, padx=3, pady=5)

    bt_contacts = Button(ctr_left, text="Contacts", command=init_functions.open_contacts, bg='seashell1',
                         activebackground='orangered1')
    bt_contacts.grid(row=2, column=1, ipady=6, ipadx=7, padx=3, pady=5)

    bt_escape = Button(ctr_left, text="Escape", command=init_functions.press_escape, bg='seashell1',
                       activebackground='orangered1')
    bt_escape.grid(row=2, column=2, ipady=6, ipadx=7, padx=3, pady=5)

    bt_volume_down = Button(ctr_left, text="Volume Down", command=init_functions.volume_down, bg='darkseagreen2',
                            activebackground='orangered1')
    bt_volume_down.grid(row=2, column=3, ipady=6, ipadx=7, padx=3, pady=5)

    bt_press_up = Button(ctr_left, text="Press UP", command=init_functions.press_action_up, bg='olivedrab3',
                         activebackground='orangered1')
    bt_press_up.grid(row=2, column=4, ipady=6, ipadx=15, padx=3, pady=5)

    bt_enter = Button(ctr_left, text="Press ENTER", command=init_functions.press_enter, bg='darkkhaki',
                      activebackground='orangered1')
    bt_enter.grid(row=2, column=5, ipady=6, ipadx=7, padx=3, pady=5)

    # Row 3
    bt_sk_keyb = Button(ctr_left, text="SK Keyboard", command=init_functions.open_soft_keyboard, bg='seashell1',
                        activebackground='orangered1')
    bt_sk_keyb.grid(row=3, column=0, ipady=6, ipadx=7, padx=3, pady=5)

    bt_settings = Button(ctr_left, text="Settings", command=init_functions.open_settings, bg='seashell1',
                         activebackground='orangered1')
    bt_settings.grid(row=3, column=1, ipady=6, ipadx=7, padx=3, pady=5)

    bt_press_menu = Button(ctr_left, text="Press Menu", command=init_functions.press_menu, bg='seashell1',
                           activebackground='orangered1')
    bt_press_menu.grid(row=3, column=2, ipady=6, ipadx=7, padx=3, pady=5)

    bt_press_left = Button(ctr_left, text="Press LEFT", command=init_functions.press_action_down, bg='olivedrab3',
                           activebackground='orangered1')
    bt_press_left.grid(row=3, column=3, ipady=6, ipadx=7, padx=3, pady=5)

    bt_press_down = Button(ctr_left, text="Press DOWN", command=init_functions.press_action_down, bg='olivedrab3',
                           activebackground='orangered1')
    bt_press_down.grid(row=3, column=4, ipady=6, ipadx=7, padx=3, pady=5)

    bt_press_right = Button(ctr_left, text="Press RIGHT", command=init_functions.press_action_down, bg='olivedrab3',
                            activebackground='orangered1')
    bt_press_right.grid(row=3, column=5, ipady=6, ipadx=7, padx=1, pady=5)

    # Row 4
    bt_contacts = Button(ctr_left, text="Contact TC", command=init_functions.open_contacts, bg='cornsilk2',
                         activebackground='orangered1')
    bt_contacts.grid(row=4, column=0, ipady=6, ipadx=7, padx=3, pady=5)

    bt_contacts2 = Button(ctr_left, text="Contact TC2", command=init_functions.open_contacts,
                          bg='cornsilk2', activebackground='orangered1')
    bt_contacts2.grid(row=4, column=1, ipady=6, ipadx=7, padx=3, pady=5)

    bt_dial = Button(ctr_left, text="DialContact", command=init_functions.test_dial_contact, bg='cornsilk2',
                     activebackground='orangered1')
    bt_dial.grid(row=4, column=2, ipady=6, ipadx=7, padx=3, pady=5)

    bt_pre_4 = Button(ctr_left, text="Precond #4", command=lambda: message_info("Precond #4"), bg='cornsilk2',
                      activebackground='orangered1')
    bt_pre_4.grid(row=4, column=3, ipady=6, ipadx=7, padx=3, pady=5)

    bt_actions = Button(ctr_left, text="Actions", command=Functions.get_commands_line, bg='cornsilk2',
                        activebackground='orangered1')
    bt_actions.grid(row=4, column=4, ipady=6, ipadx=7, padx=3, pady=5)

    bt_timer = Button(ctr_left, text="TIMER", command=init_functions.timer, bg='cornsilk2',
                      activebackground='orangered1')
    bt_timer.grid(row=4, column=5, ipady=6, ipadx=7, padx=3, pady=5)
    # Image display
    Label(ctr_right, image=img).pack()
    gui.mainloop()


# scrolling
gui.grid_rowconfigure(1, weight=1)
gui.grid_columnconfigure(0, weight=1)

# Welcome screen
intro_center = Frame(gui, width=700, height=600)
intro_center.grid(row=0, sticky="n")

# Background image
background_label = Label(intro_center, image=img_welcome_view)
background_label.grid(row=0, column=0, sticky="NSEW")


def initialize_driver(init_driver):
    """Initialize driver."""
    if init_driver == driver.create_wifi_driver:
        create_driver = driver.create_wifi_driver(
            {'newCommandTimeout': data["newCommandTimeout"], "deviceId": data["wifi"]["device_id"]})
        init_functions = Functions.Functions(create_driver)

    elif init_driver == driver.create_usb_driver:
        create_driver = driver.create_usb_driver(
            {'newCommandTimeout': data["newCommandTimeout"], "deviceId": data["usb"]["device_id"]})
        init_functions = Functions.Functions(create_driver)

    else:
        create_driver = driver.create_avd_driver({'newCommandTimeout': data["newCommandTimeout"]})
        init_functions = Functions.Functions(create_driver)

    return create_driver, init_functions


# Dropdown Menu in Welcome screen
driver = driver_server.Driver()
driver_options = {"avd": driver.create_avd_driver, "usb_driver": driver.create_usb_driver,
                  "wifi_driver": driver.create_wifi_driver}

init_variable = StringVar(intro_center)
init_variable.set("Select device")  # default value
new_driver = driver


def change_driver(options):
    """Method to select specific driver."""
    global new_driver
    new_driver = driver_options[options]


# driver instance
dropdown = OptionMenu(intro_center, init_variable, *driver_options.keys(), command=change_driver)
dropdown.grid(row=0, column=0, ipadx=5, pady=160, sticky="N")

# Buttons configuration
bt_connect = Button(intro_center, text="CONNECT", command=lambda: driver_init(new_driver), bg='greenyellow',
                    font=("Times New Roman", 15))
bt_connect.grid(row=0, column=0, ipadx=20, pady=110, sticky="N")
bt_exit = Button(intro_center, text="Exit", command=exit_now, bg='firebrick2', font=("Times New Roman", 12))
bt_exit.grid(row=0, column=0, ipadx=30, pady=220, sticky="N")

bt_authors = Button(intro_center, text="Authors", command=message_authors, bg='#FF7D40', font=("Times New Roman", 7))
bt_authors.grid(row=0, column=0, ipadx=2, padx=80, pady=80, sticky="SE")

# MAIN APP GUI START and REFRESH
gui.mainloop()

