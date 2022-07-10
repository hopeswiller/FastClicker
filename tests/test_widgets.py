import pytest
from tkinter import Tk, Menu, Entry, LabelFrame, Button
from src.widgets import *

# widgets -------------------------------------------------------------------------


def test_get_menu_bar(window):
    item1, item2 = get_menu_bar(window)
    assert isinstance(item1, Menu) and isinstance(item2, Menu)


def test_set_window(window):
    set_window(window, width=612, height=510, resizable=False)
    assert int(window.winfo_width()) == 612 and int(window.winfo_height()) == 510


def test_get_cursor_options_items(window):
    (
        cursorFrame,
        path,
        loadBtn,
        reloadBtn,
        pickBtn,
    ) = get_cursor_options_items(window)
    assert isinstance(cursorFrame, LabelFrame) and isinstance(path, Entry)
