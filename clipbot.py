import requests, os, clipboard, sys, webbrowser, configparser
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QApplication

# chat = "679657858"
# bot_token = "839117531:AAFNWM8soA-V-sPes7iXQzl18KSaS34fWKI"

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

def send_clipboard():
    response = requests.get('https://api.telegram.org/bot' + str(get_token()) + '/sendMessage?chat_id=' + str(get_chat()) + '&parse_mode=Markdown&text=' + clipboard.paste())
    if response.json()['ok'] == True:
        os.system('notify-send "clipbot" "Clipboard has been sent via Telegram bot."')
    else:
        os.system('notify-send "clipbot" "Couldnt send message (' + str(response.status_code) + '): ' + response.json()['description'] + '."')


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        self.installEventFilter(self)
        self._send_action = menu.addAction("Send Clipboard", self.on_send_click)
        self._preferences_action = menu.addAction("Preferences", self.on_preferences_click)
        self._exit_action = menu.addAction("Exit", self.on_exit_click)
        self.setContextMenu(menu)

        self.activated.connect(self.on_item_click)
        self.show()

    def on_exit_click(self):
        print("Exit clicked")
        exit(0)
    
    def on_send_click(self):
        send_clipboard()

    def on_preferences_click(self):
        print("Preferences clicked!")
        self.prefWindow = Preferences()

    def on_item_click(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            print("Icon clicked!")

class Preferences(QtWidgets.QMainWindow):
    def __init__(self):
        super(Preferences, self).__init__()
        uic.loadUi('preferences.ui', self) # Load the UI file
        self.lineEdit.setText(get_token())
        self.lineEdit_2.setText(get_chat())

        if self.lineEdit.text() == "" or self.lineEdit_2.text() == "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.save)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Help).clicked.connect(self.help)

        self.lineEdit.textChanged.connect(lambda: self.check_textbox(self.lineEdit))
        self.lineEdit_2.textChanged.connect(lambda: self.check_textbox(self.lineEdit_2))
        self.show()

    def check_textbox(self, textbox):
        if self.lineEdit.text() == "" or self.lineEdit_2.text() == "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
    def save(self):
        set_chat(self.lineEdit_2.text())
        set_token(self.lineEdit.text())
        self.close()
        print("Saved new credentials.")
    def cancel(self):
        self.close()
    def help(self):
        webbrowser.open('https://github.com/realmayus/clipbot/README.md')
        print("Opened browser window with URL https://github.com/realmayus/clipbot/README.md")

class SystemTrayApp:
    def __init__(self):
        self.event_exit_app = None

        self._app = QtWidgets.QApplication(sys.argv)
        self._app.setQuitOnLastWindowClosed(False) # dont quit when the last window (preferences) has been closed
        self._widget = QtWidgets.QWidget()
        self._icon = SystemTrayIcon(QtGui.QIcon("icon.png"), self._widget)
    def run(self):
        sys.exit(self._app.exec_())


SystemTrayApp().run()
