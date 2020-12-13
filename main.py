#!/usr/bin/python
"""
    Phone Witnessing Tool v2.0
    Raymond Hernandez
    December 10, 2020

    Revision History:
        2.0 - Full feature that includes parsed data displayed in the text field.
              New GUI to display all query fields created with QT Designer.
        1.2 - Improved bugs and UI coded in Java.  New GUI by JSwing.
        1.1 - Added a phone number formatter to remove non-numeric characters
        1.0 - First release that opens links upon search
"""
import sys
from GUI import *
from web_scrapper import *


class PhoneWitnessingTool(Ui_root):
    def __init__(self, window):
        self.setupUi(window)

        self.button_search.clicked.connect(self.clicked_search_button)
        self.button_view_map.clicked.connect(self.clicked_check_map)
        self.button_captcha.clicked.connect(self.clicked_reCaptcha)

    def clicked_reCaptcha(self):
        webbrowser.open_new("https://www.truepeoplesearch.com/InternalCaptcha?returnUrl=%2fresultphone%3fphoneno%3d")

    def clicked_search_button(self):
        query = self.search_field.text()
        query = format_number(query)

        if len(query) == 10:
            globals.SYSTEM_MSG = "Searching database.  Please wait...."
            self.label_status.setText(globals.SYSTEM_MSG)
            self.search_now(query)
        if query == '0':
            globals.SYSTEM_MSG = "Invalid phone number."
            self.label_status.setText(globals.SYSTEM_MSG)

            self.field_full_name.setText("")
            self.field_age.setText("")
            self.field_demographic.setText("")
            self.field_address.setText("")
            self.field_other_phones.setText("")
            self.field_relatives.setText("")

    def search_now(self, query):
        generate_report(query)

        if not globals.NO_CAPTCHA_NEEDED:
            self.label_status.setText(globals.SYSTEM_MSG)

        else:
            self.field_full_name.setText(globals.NAME)
            self.field_age.setText(globals.AGE)
            self.field_demographic.setText(globals.COUNTRY)
            self.field_address.setText(globals.ADDRESS)
            self.field_other_phones.setText(globals.PHONES)
            self.field_relatives.setText(globals.RELATIVES)

            if globals.TASK_COMPLETED:
                self.label_status.setText(globals.SYSTEM_MSG)

    def clicked_check_map(self):
        if not globals.ADDRESS:
            webbrowser.open_new("https://www.google.com/maps")
        open_google_map(globals.ADDRESS)


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = PhoneWitnessingTool(MainWindow)
    MainWindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
