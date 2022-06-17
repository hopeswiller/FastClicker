# Ensuring consistent coordinates between listener and controller on Windows
# Recent versions of _Windows_ support running legacy applications scaled
# when the system scaling has been increased beyond 100%.

# This allows old applications to scale, albeit with a blurry look, and avoids tiny, unusable user interfaces.

# This scaling is unfortunately inconsistently applied to a mouse listener and a controller:
# the listener will receive physical coordinates, but the controller has to work with scaled coordinates.
# This can be worked around by telling Windows that your application is DPI aware.
# This is a process global setting, so _pynput_ cannot do it automatically.
# Do enable DPI awareness

import ctypes

PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
