# dartscore
A Python app to implement a simple darts scoreboard using a Raspberry Pi with a
touch display.

### Quick start
I haven't put much (any) effort into packaging this, so you need to clone the
repository and run it from the command line or an IDE. The target environment
is a Raspberry Pi, but Python and Qt are available across platforms and the 
app works on Windows, Mac and Linux. The following commands were tested on
a fresh install of Linux Mint Cinnamon 22.2, but you should be able to tweak
them for your own environment.

    apt install -y git python3-pip python3-venv libxcb-cursor0
    git clone https://github.com/johnreah/dartscore.git
    cd dartscore
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python main.py

### Design notes

### Python notes
[Python tutorial on virtual environments and Packages](https://docs.python.org/3/tutorial/venv.html)

Useful python commands (for Windows):
* <code>python -m venv .venv</code> creates virtual environment in .venv directory
* <code>.venv\Scripts\activate</code> activates virtual environment
* <code>deactivate</code> deactivates virtual environment
* <code>python -m pip install PyQt6</code> installs PyQt6 module
* <code>python -m pip freeze > requirements.txt</code>
* <code>python -m pip install -r requirements.txt</code>

Significant difference for Linux/Mac:
* <code><u>source</u> .venv/<u>bin</u>/activate</code>

### To do list
* ~~Create project in GitHub~~
* ~~Include housekeeping files like .gitignore~~
* ~~Create virtual environment~~
* ~~Add modules such as PyQt6~~
* ~~Add requirements.txt~~
* ~~Verify successful deployment on Raspberry Pi (and Mac)~~
* ~~Create placeholder alternative keypad widget~~
* ~~Wrap alternative keypads in tab widget~~
* ~~Adopt 7-segment font for scores~~
* ~~Factor out font into parent stylesheet~~
* ~~Experiment with bitmpas for buttons~~
* ~~Implement by-total score editing~~
* ~~Widgetise keypad - send signals for output~~
* Review widget sizes using fixed dimensions where appropriate
* Experiment with background in keeping with the visual theme
* Park score-by-dart for a later version
* Implement basic gameplay (reset, turns, etc.)
* Write and test copy-paste deployment notes

### Links I found useful

https://share.google/iP07d78l5hV7fZdEh

http://neatnik.net/adam/bucket/numeric-keypad-iie/

https://www.keyboard-layout-editor.com/

