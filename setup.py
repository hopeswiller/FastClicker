import sysconfig, sys, os
import uuid
from cx_Freeze import setup, Executable

version = "1.0.4"
app_name = "FastClicker"

# Generate a UUID (GUID) for the Upgrade Code
code = str(uuid.uuid3(uuid.NAMESPACE_DNS, f'{version.lower()}.hopeswiller.org')).upper()
UPGRAGE_CODE = "{%s}" % (code)

programfiles_dir = 'ProgramFiles64Folder' if sysconfig.get_platform() == 'win-amd64' else 'ProgramFilesFolder'
initial_target_dir = '[%s]\%s\%s' % (programfiles_dir, app_name, f'v{version}')

bdist_msi_options = {
    "add_to_path": False,
    "install_icon": "./assets/icon.ico",
    "target_name": app_name,
    "summary_data": {"author": "hopeswiller"},
    'initial_target_dir': initial_target_dir,
    "upgrade_code": UPGRAGE_CODE
}

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["src"],
    "includes": ["pynput.keyboard._win32", "pynput.mouse._win32"],
    "include_files": ["./assets/icon.ico", "./assets/template.xlsx"],
    "include_msvcr": True
}


# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name=app_name,
    version=version,
    author="hopeswiller",
    author_email="davidba941@gmail.com",
    description=f"{app_name} By Hopeswiller<davidba941@gmail.com>",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[
        Executable(
            script="app.py",
            target_name=app_name,
            copyright=f"Copyright (C) 2022 {app_name}",
            base=base,
            icon="./assets/icon.ico",
            uac_admin=True,
            shortcut_name=app_name,
            shortcut_dir="ProgramMenuFolder"
            # shortcut_dir=StartupFolder
        ),
    ],
)
