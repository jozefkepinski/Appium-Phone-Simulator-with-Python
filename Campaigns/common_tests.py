"""Campaing Common Test_Cases."""

import driver_server
import json
from Test_Cases import dial_contact, open_close_contacts

# Load Config file
with open(f"../config/avd.json") as config_file:
    data = json.load(config_file)

print("Connecting driver...")
driver = driver_server.Driver()
create_driver = driver.create_avd_driver({'newCommandTimeout': data["newCommandTimeout"]})
print("Driver connected.")

#  Test Cases to run
Test_Case_Open_close_Contacts = open_close_contacts.OpenCloseContacts(create_driver)
Test_Case_Open_close_Contacts.open_close_contacts()

Test_Case_Dial_Contacts = dial_contact.DialContact(create_driver)
Test_Case_Dial_Contacts.test_dial_contact()
