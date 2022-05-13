import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": ["src"],
    "includes": ["pynput.keyboard._win32", "pynput.mouse._win32"],
    "include_files": ["profile.xlsx"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="AutoClicker",
    version="0.1",
    author="hopeswiller",
    author_email="davidba941@gmail.com",
    description="My AutoClicker application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/clicker.py", base=base)],
)
