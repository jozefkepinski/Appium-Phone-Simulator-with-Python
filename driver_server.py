# import logging

import json
import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService


class Driver:
    """Class contain only function blocks."""

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Load AVD Config file
    with open(f"{ROOT_DIR}\\config\\common.json") as config_file:
        common = json.load(config_file)

    "Appium service connection data"
    _APPIUM_PORT = common["appium_port"]
    _APPIUM_HOST = common["appium_host"]

    def appium_service(self):
        """Function which preparing connection with Phone"""
        service = AppiumService()
        service.start(
            args=['--address', self._APPIUM_HOST, '-p', str(self._APPIUM_PORT)],
            timeout_ms=20000, )
        yield service
        service.stop()

    def android_driver_factory(self):
        """This is a creator in case that new devices configs will be available in the future"""
        return self.create_avd_driver()

    def create_avd_driver(self, custom_opts=None):
        """Function which realize connection with Phone according to provided data OPTIONS"""

        options = UiAutomator2Options()
        options.platformName = self.common["avd"]["platformName"]
        print(f"platformName: {self.common['avd']['platformName']}")
        options.platformVersion = self.common["avd"]["platformVersion"]
        print(f"platformVersion: {self.common['avd']['platformVersion']}")
        options.deviceName = self.common["avd"]["deviceName"]
        print(f"deviceName: {self.common['avd']['deviceName']}")
        options.automationName = self.common["avd"]["automationName"]
        print(f"automationName: {self.common['avd']['automationName']}")
        options.avd = self.common["avd"]['avd']
        print(f"avd: {self.common['avd']['avd']}")

        if custom_opts is not None:
            options.load_capabilities(custom_opts)
        return webdriver.Remote(f'http://{self._APPIUM_HOST}:{self._APPIUM_PORT}', options=options)

    def create_wifi_driver(self, custom_opts=None):
        """Function which realize connection with Phone according to provided data OPTIONS"""

        options = UiAutomator2Options()
        options.platformName = self.common["wifi"]['platformName']
        print(f"platformName: {self.common['wifi']['platformName']}")
        options.platformVersion = self.common["wifi"]['platformVersion']
        print(f"platformVersion: {self.common['wifi']['platformVersion']}")
        options.deviceName = self.common["wifi"]['deviceName']
        print(f"deviceName: {self.common['wifi']['deviceName']}")
        options.automationName = self.common['wifi']['automationName']
        print(f"automationName: {self.common['wifi']['automationName']}")

        if custom_opts is not None:
            options.load_capabilities(custom_opts)
        return webdriver.Remote(f'http://{self._APPIUM_HOST}:{self._APPIUM_PORT}', options=options)

    def create_usb_driver(self, custom_opts=None):
        """Function which realize connection with Phone according to provided data OPTIONS"""

        options = UiAutomator2Options()
        options.platformName = self.common['usb']['platformName']
        print(f"platformName: {self.common['usb']['platformName']}")
        options.platformVersion = self.common["usb"]['platformVersion']
        print(f"platformVersion: {self.common['usb']['platformVersion']}")
        options.deviceName = self.common["usb"]['deviceName']
        print(f"deviceName: {self.common['usb']['deviceName']}")
        options.automationName = self.common["usb"]['automationName']
        print(f"automationName: {self.common['usb']['automationName']}")

        if custom_opts is not None:
            options.load_capabilities(custom_opts)
        return webdriver.Remote(f'http://{self._APPIUM_HOST}:{self._APPIUM_PORT}', options=options)
