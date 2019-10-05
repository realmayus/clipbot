import requests, os, clipboard, sys, webbrowser, configparser
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QApplication

#####
# Config
#####
def get_token():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config['config']['token']

def set_token(new_token: str):
    config = configparser.ConfigParser()
    config.read("config.ini")
    section = config['config']
    section['token'] = new_token
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def get_chat():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config['config']['chat'] 

def set_chat(new_chat: str):
    config = configparser.ConfigParser()
    config.read("config.ini")
    section = config['config']
    section['chat'] = new_chat
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

######
# Actual API calls
######
def send_clipboard():
    response = requests.get('https://api.telegram.org/bot' + str(get_token()) + '/sendMessage?chat_id=' + str(get_chat()) + '&parse_mode=Markdown&text=' + clipboard.paste()) # Executing the API call, sending telegram the clipboard's contents
    if response.json()['ok'] == True: # Response is "ok"
        os.system('notify-send "clipbot" "Clipboard has been sent via Telegram bot."') # Sending success message to OS
    else: # Response is not "ok"
        os.system('notify-send "clipbot" "Couldnt send message (' + str(response.status_code) + '): ' + response.json()['description'] + '."') # Sending Notification to OS with error and -code

######
# UI Stuff
######
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)

        menu = QtWidgets.QMenu(parent) # Creating a menu
        self._send_action = menu.addAction("Send Clipboard", self.on_send_click) # Adding tray menu items
        self._preferences_action = menu.addAction("Preferences", self.on_preferences_click) # ^
        self._exit_action = menu.addAction("Exit", self.on_exit_click) # ^
        self.setContextMenu(menu) # Setting the context menu

        self.show() # Displaying the system tray menu

    def on_exit_click(self): # User clicked on "Exit" tray menu item
        print("Exit clicked")
        exit(0) # Terminating clipbot
    
    def on_send_click(self): # User clicked on "Send Clipboard" tray menu item
        send_clipboard()

    def on_preferences_click(self): # User clicked on "Preferences" tray menu item
        print("Preferences clicked!")
        self.prefWindow = Preferences()

class Preferences(QtWidgets.QMainWindow):
    def __init__(self):
        super(Preferences, self).__init__()
        uic.loadUi('preferences.ui', self) # Load the UI file
        self.lineEdit.setText(get_token()) # Setting the content of the text boxes to the values stored in the config
        self.lineEdit_2.setText(get_chat()) # ^
        self.setWindowIcon(QtGui.QIcon("icon.png")) # Setting Preferences Window Icon

        if self.lineEdit.text() == "" or self.lineEdit_2.text() == "": # Disabling "Save" button when one or both text boxes are empty
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.save) # Connecting the button clicked events
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel) # ^
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Help).clicked.connect(self.help) # ^

        self.lineEdit.textChanged.connect(lambda: self.check_textbox(self.lineEdit)) # Connecting the textChanged Event to chech_textbox()
        self.lineEdit_2.textChanged.connect(lambda: self.check_textbox(self.lineEdit_2)) # Connecting the textChanged Event to check_textbox()
        self.show() # Displaying/Opening the preferences window

    def check_textbox(self, textbox): # Disabling "Save" button when one or both text boxes are empty
        if self.lineEdit.text() == "" or self.lineEdit_2.text() == "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)

    def save(self): # User clicked on save button
        set_chat(self.lineEdit_2.text()) # Setting config values to values in text boxes
        set_token(self.lineEdit.text()) # ^
        self.close() # Closing pref window
        print("Saved new credentials.") # Logging a credentials change

    def cancel(self): # User clicked on cancel button
        self.close() # Closing the pref window

    def help(self): # User clicked on Help button
        webbrowser.open('https://github.com/realmayus/clipbot/blob/master/README.md') # Opening a web browser window with the README.md page for help
        print("Opened browser window with URL https://github.com/realmayus/clipbot/blob/master/README.md")

class SystemTrayApp:
    def __init__(self):
        self.event_exit_app = None

        self._app = QtWidgets.QApplication(sys.argv)
        self._app.setQuitOnLastWindowClosed(False) # dont quit when the last window (preferences) has been closed
        self._widget = QtWidgets.QWidget()
        self._icon = SystemTrayIcon(QtGui.QIcon("icon.png"), self._widget) # Creating instance of SystemTrayIcon (Parent UI Element)
    def run(self):
        sys.exit(self._app.exec_())


SystemTrayApp().run()
