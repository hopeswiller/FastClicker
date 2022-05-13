import logging
from datetime import datetime
from pyfiglet import Figlet


def init_logging():
    log = logging.getLogger(__name__)
    log_format = "%(asctime)s %(levelname)s %(module)s::%(funcName)s || %(message)s"
    logging.basicConfig(
        level=logging.DEBUG, format=log_format, datefmt="%Y-%m-%d %H:%M:%S"
    )
    return log


def init_figlet():
    figlet = Figlet()
    print(f"Application Started: {datetime.now()}")
    print(f"- Start/Stop Clicking: F4 Key\n- Exit App: Esc key")
    print(figlet.renderText("AutoClicker"))
