# Session Noter

<p align="left">
    <a href="https://circleci.com/gh/j19sch/session-noter/tree/master">
        <img src="https://circleci.com/gh/j19sch/session-noter/tree/master.svg?style=svg" alt="CircleCI status"/></a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black code formatter"/></a>
    <a href="https://github.com/j19sch/session-noter/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="MIT license"/></a>
</p>

Small suite of note-taking tools for session-based test management (SBTM)


## What to do with it

### Setup & installation
- grab a copy of this repo, i.e. download, clone or fork
- make sure you have Python 3.6 or higher (`python -V` or `python3 -V`)
- create a virtual environment and activate it: <https://docs.python.org/3/tutorial/venv.html>
- install dependencies with `pip install -r requirements.txt`

### Usage
In the `./session_noter` directory:
- `python session-noter.py` - record session notes
    - prompt `(ntr 0/45 0.0%)`: 0 of 45 minutes elapsed, i.e. 0.0%
- `python session-printer.py <file>` - convert session notes files to markdown
- `python session-analyzer.py <file or files>` - summarize session notes file(s) in markdown


## Core design ideas
- support for linux, mac, windows
- everything is configurable
- plug-in support: additional interfaces, additional output formats, etc.


## More on SBTM
- <http://www.satisfice.com/articles/sbtm.pdf>
- <http://www.satisfice.com/sbtm/>
