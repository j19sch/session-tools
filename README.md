# Session Noter

Python package to play around with:
- interfaces (text-based and graphical)
- data processing and reporting
- modularity and plugins
- meta-programming

Purpose of the package as such is to support session-based test management (SBTM) - inspired by Shmuel Gershon's Rapid Reporter (http://testing.gershon.info/reporter/).


## The plan

### Functionality
- session-noter: recording session notes
- session-printer: exporting/printing notes in different formats (md, html, ...)
- session-analyzer: analyzing session notes

### Interfaces
- CLI
- curses
- GUI (minimal floating and full)

### Architecture
- support for Linux, Mac, Windows
- everything is configurable
- pluggable: additional interfaces, additional exporters, etc.