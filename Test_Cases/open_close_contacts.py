"""Open contacts, go to main screen Test_Case."""

from Functions import Functions


class OpenCloseContacts(Functions):
    """Contain Common Test_Cases for android device."""
    def __init__(self, driver):
        super().__init__(driver)

    def open_close_contacts(self):
        """TestCase : Open Contacts context, then go HOME screen context, repeat both steps"""
        Functions.open_contacts(self)
        Functions.press_home(self)
        Functions.open_contacts(self)
        Functions.press_home(self)
