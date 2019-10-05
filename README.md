# clipbot
A small, lightweight python app that sends you your clipboard via Telegram. Only One click! Fancy GUIs!


## Features
* Allows you to send your clipboard to your phone, tablet etc. in just one click!
* System Tray icon for easy-peasy access
* Preferences GUI to change your bot tokens and chat IDs

## Planned
* Support for more than one chat ID

## How to Install / Use
0. Make sure that you have Python 3.x and PIP for that version as well as `git`
1. `cd` into the cloned repository
2. Clone this project with `git clone https://github.com/realmayus/clipbot.git`
3. Install all mandatory packages with `pip3 install -r "requirements.txt"`
   (if `pip3` isn't found, try `pip`)
4. Create a file called config.ini with this content:
  ```ini
  [config]
  token = 
  chat  
  ```
5. Open the main file with `python3 clipbot.py`
6. You should now see a clipboard icon in your system tray. Depending on your OS, it might be at the top right of your screen or at the bottom right.
7. Click that icon and then on "Preferences"
8. Fill out the Bot Token and ChatID fields ([How to get those values]())
9. Click on "Save"
10. Copy something to your clipboard and then click the icon in your system tray and click "Send Clipboard"
11. Done! Profit!
