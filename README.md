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
This started as a quick Christmas holiday project and was triggered partly by the
World Darts Championship that was happening at the time and partly by my partner
giving me a dartboard (to replace the one I lent my brother 15 years ago and
haven't seen since). The UI design was inspired by a pub darts scoreboard I
used to use about 20 years ago, and the choice of target hardware was heavily
influenced by what was in my box of single board computers that included a
Raspberry Pi 3B (the earliest wi-fi model). I added the official 7" touch
display out of curiosity. Software-wise I picked Python because of the rapid
edit/debug cycle, and Qt because it's cross-platform and I wanted to learn it.

The visual aspect of the UI came together quite quickly, and the "business logic"
isn't too complicated. The vast majority of the development effort was 
necessitated by a pull request made by my pal Chris who had used his assistant
Claude to add button click sounds and some text-to-speech features. This wasn't 
part of my original plan, as my Pi has no sound output device, but once the 
challenge had been laid down I couldn't very well say no. This was a big mistake.

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
* ~~Experiment with background in keeping with the visual theme~~
* ~~Write and test copy-paste deployment notes~~
* ~~Refactor player widgets into array to reduce code duplication~~ 
* Review widget & layout sizes using fixed dimensions where appropriate
* Implement basic gameplay (reset, turns, etc.)
* Implement audio output from Chris's pull request
* Write deployment notes for Raspberry Pi (screen orientation, auto-login)
* Revisit score entry by-dart for a later version

### Links I found useful

https://share.google/iP07d78l5hV7fZdEh

http://neatnik.net/adam/bucket/numeric-keypad-iie/

https://www.keyboard-layout-editor.com/

https://www.youtube.com/watch?v=BAx4N4QtkeY

https://python-sounddevice.readthedocs.io/en/0.5.3/usage.html

