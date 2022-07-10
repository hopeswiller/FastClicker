import pytest
from src.autoclick import AutoClicker
from tkinter import Tk


@pytest.fixture()
def window():
    root = Tk()
    return root


@pytest.fixture()
def filepath():
    return "tests\\resources\\test_template.xlsx"


@pytest.fixture()
def expected_headers():
    return {"Activity": None, "X": None, "Y": None, "Button": None, "delay(s)": None}


@pytest.fixture()
def expected_profile():
    return [
        {"Activity": "refresh", "X": 58, "Y": 847, "Button": "L", "delay(s)": 5},
        {"Activity": "order", "X": 58, "Y": 547, "Button": "R", "delay(s)": 8},
    ]


@pytest.fixture()
def TestAutoClicker(AutoClicker):
    super().__init__()
    self.profile = [
        {"Activity": "refresh", "X": 58, "Y": 847, "Button": "L", "delay(s)": 5},
        {"Activity": "order", "X": 58, "Y": 547, "Button": "R", "delay(s)": 8},
    ]
