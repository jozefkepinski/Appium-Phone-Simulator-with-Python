""""""

from Functions import Functions
from appium.webdriver.common.appiumby import AppiumBy


class DialContact(Functions):
    """Contain Common Test_Cases for android device."""
    def __init__(self, driver):
        super().__init__(driver)

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