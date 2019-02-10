# Session Noter

Small suite of tools for session-based test management (SBTM)


## What to do with it

### Setup & installation
- grab a copy of this repo, i.e. download, clone or fork
- install Python 3
- create a virtual environment and activate it: https://docs.python.org/3/tutorial/venv.html
- install `requirements.txt`

### Usage
In the `./session_noter` directory:
- `python session-noter.py` - record session notes
    - prompt `(ntr 0/45 0.0%)`: 0 of 45 minutes elapsed, i.e. 0.0%
- `python session-printer.py <file>` - convert session notes files to markdown
- `python session-analyzer.py <file or files>` - summarize session notes file(s) in markdown


## What's left to do
- config file validation
- auto-tests
- note types configurability in printer and analyzer
- interfaces beside CLI
- much much more


## What I was thinking

### Core design ideas
- support for linux, mac, windows
- everything is configurable
- plug-in support: additional interfaces, additional output formats, etc.

### My learning goals
- interfaces (cli, curses, gui)
- data processing and reporting
- modularity and plugins
- meta-programming


## More on SBTM
- http://www.satisfice.com/articles/sbtm.pdf
- http://www.satisfice.com/sbtm/
