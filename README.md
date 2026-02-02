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
Raspberry Pi 3B (the earliest Wi-Fi model). I added the official 7" touch
display out of curiosity. Software-wise I picked Python because of the rapid
edit/test/debug cycle, and Qt because it's cross-platform and I wanted to learn
it.

The visual aspect of the UI came together quite quickly, and the "business logic"
isn't too complicated. The vast majority of the development effort was 
necessitated by a pull request made by my pal Chris who had used his assistant
Claude to add button click sounds and some text-to-speech features. This wasn't 
part of my original plan, as my Pi has no sound output device, but once the 
challenge had been laid down I couldn't very well say no. This was a big mistake.

The code written by Claude used pyttsx3 and put the text-to-speech code in a
background worker thread. This was a great plan, but although it worked fine
on MacOS it dropped utterances on Windows, so I didn't get as far as testing it
on the Pi. Because the app uses Qt and I have a background that stretches back
to Windows 3.1, I decided to rewrite using cooperative multitasking based on
the Qt event loop. This was clean and worked perfectly on MacOS and Windows,
but failed on the Pi. According to my own assistant Grok this is a shortcoming
of the Pi's implementation of espeak. I'd had enough of pyttsx3 by this point,
so I decided try out piper-tts (Grok's choice) and use Qt's QThread as the
background worker. This was a bit of a learning curve, and there's a bit of a 
dance to be performed in connecting the Qt signals and slots, but it worked
in the end. Downsides of the approach: piper-tts is a lot more heavyweight
than pyttsx3, and it introduces a noticeable though not unbearable delay on
the Pi 3B. It also seems sensitive to the version of onnxruntime. The upside
is that the speech quality of piper-tts is very good.

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

[Pigar](https://pypi.org/project/pigar/) is a handy way of generating a
requirements.txt file. It works by scanning the imports in your source code,
and it produces a short list of the modules that you've installed,
unlike `pip freeze` which includes all the dependenices too. I know I
haven't fully understood this topic, but it seems to work well.

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
* ~~Implement basic gameplay (reset, turns, etc.)~~
* ~~Implement audio output from Chris's pull request~~
* Write deployment notes for Raspberry Pi (screen orientation, auto-login, Wayland)
* Fix Raspberry Pi to wall next to dartboard (dependency - fix dartboard to wall)
* Revisit score entry by-dart for a later version

### Links I found useful

https://share.google/iP07d78l5hV7fZdEh

http://neatnik.net/adam/bucket/numeric-keypad-iie/

https://www.keyboard-layout-editor.com/

https://www.youtube.com/watch?v=BAx4N4QtkeY

https://python-sounddevice.readthedocs.io/en/0.5.3/usage.html

