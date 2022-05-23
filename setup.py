import os, sys
import uuid
from cx_Freeze import setup, Executable

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

version = "1.0.0"
# Generate a UUID (GUID) for the Upgrade Code
UPGRAGE_CODE = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'autoclicker.hopeswiller.org')).upper()

initial_target_dir = os.path.join("ProgramFilesFolder",'AutoClicker',version)
bdist_msi_options = {
    "add_to_path": True,
    "install_icon": "icon.ico",
    "target_name": f"AutoClicker.{version}",
    "summary_data": {"author": "hopeswiller"},
    'initial_target_dir': initial_target_dir,
    "upgrade_code": "{%s}".format(UPGRAGE_CODE),
    "data": {
        # "Directory": [
        #     ("ProgramMenuFolder", "TARGETDIR", "."),
        # #     # ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
        # ],
        "ProgId": [("Prog.Id", None, None, "This is a description", "IconId", None)],
        "Icon": [("IconId", "icon.ico")],
    },
}

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["src"],
    "includes": ["pynput.keyboard._win32", "pynput.mouse._win32"],
    "include_files": ["icon.ico"],
    "include_msvcr": True
}


setup(
    name="AutoClicker",
    version=version,
    author="hopeswiller",
    author_email="davidba941@gmail.com",
    description="AutoClicker By Hopeswiller<davidba941@gmail.com>",
    options={
        "build_exe": build_exe_options,
        # "bdist_msi": bdist_msi_options,
    },
    executables=[
        Executable(
            script="app.py",
            target_name=f"AutoClicker.{version}",
            copyright="Copyright (C) 2022 AutoClicker",
            base=base,
            icon="icon.ico",
            shortcut_name=f"AutoClicker.{version}",
            shortcut_dir="DesktopFolder",
        ),
    ],
)
