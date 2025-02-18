# OkieGuessr
A simple Python program which can be essentially used as a "guess the number" game, but instead of numbers, it uses donation goals. This program was developed from an idea for the Okie Gaming channel on YouTube.

Features:
* A display of the current possible bets
* A log file which contains financial info: the average income and actual income per session
* An encrypted session data file: this allows for the continuation of the previous session and prevents tampering

Once a new session has been started, and a valid bet has been placed, it will overwrite the previous session data file. Bets which are not included in the current possible bets list will also count towards the actual income of the session. Both the log and session data file will be created in the same directory of the `OkieGuessr.exe` file. 

Download `OkieGuessr.exe` from the `dist` directory to use the program. Your operating system or antivirus program will most likely consider it a threat: just ignore that (for more information, look [here](https://www.reddit.com/r/learnpython/comments/e99bhe/comment/fahcknk/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)).

The .exe file was created with pyinstaller. It is quite big for the simplicity of the program since it includes a lot of modules in the .exe file.

Author: Cédric (@cedric10012002)
