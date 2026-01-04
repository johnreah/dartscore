# dartscore
Python app to track darts scores using a Raspberry Pi touch display.

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
* Adopt 7-segment font for scores
* Review widget sizes using fixed dimensions where appropriate
* Factor out font into parent stylesheet
* Experiment with bitmpas for buttons
* Implement by-total score editing
* Widgetise keypad - send signals for output
* 