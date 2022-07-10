# FastClicker

> Automatic Clicking Application with predefined template


## Table of contents

<!-- - [General info](#general-info) -->
<!-- - [Screenshots](#screenshots) -->
- [Technologies](#technologies)
- [Setup](#setup)
- [Features](#features)
- [Status](#status)


## Technologies
_Major packages used_
```
Python 3.9.*
Tkinter Framework
Pynput = "1.7.6"
Openpyxl = "3.0.10"
```

## Setup

+ Run ```make help``` to know the available commands to run
+ Run ```make create-setup-env``` to create setup a virtual environment
+ Run ```make run-app``` to start the application

## Features

List of features ready and TODOs for future development

- [x] An executable to run application
- [x] Application made to alsways stay active on every window
- [x] Load Cursor Positions from a file (.xlsx)
- [x] Start clicking the cursor positions 
- [x] Stop clicking the cursor positions 
- [x] Sample template available in installation folder to load cursor positions
- [x] Save data loaded to the application to a file
- [x] Edit already loaded data (mouse positions)
- [x] Pick Mouse Locations
- [x] Application is DPI aware
- [x] Use of mutliple threads for processing
- [x] Added testcase using pytest

TODOs:

- [x] Refactor code
- [x] Fix minor issues/bugs

REMOVED:

- [x] Download a sample template to load cursor positions

## Status

Project is: _in progress_
