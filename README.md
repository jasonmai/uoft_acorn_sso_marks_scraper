# University of Toronto ACORN SSO Marks Scraper

This is a simple script/tool that simulates SSO (single sign-on) login, then scrapes your marks from ACORN. Python's `requests` library is necessary for this to work so you may need to `pip install requests`.

## Requirements
 - You need a computer
 - You need to power on the computer
 - You need an ACORN account
 - You need Python 2.7 or Python 3
 - You need Python's `requests` library

## Installation
 - `pip install requests`
 - Download the correct version of the script, corresponding to your Python version (2.7/3).
 
## Usage
 - Run script in terminal (preferred) through: `python acorn_marks.py`.
   - You may run the script from your IDE. However, your password may not be masked when inputting.
 - Enter your ACORN credentials
   - You may hardcode your credentials at the top of the script (though not recommended) - global variables USERNAME and PASSWORD. You won't be prompted to input credentials after this.
 - Marks and GPA information will populate the terminal
