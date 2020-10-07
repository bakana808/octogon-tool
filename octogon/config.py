"""
Octogon Panel Constants
"""
import os
import logging
from colorama import Fore, Style

cwd = os.getcwd()

logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.ERROR, "ERR")
logging.addLevelName(logging.CRITICAL, "CRIT")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(
    logging.Formatter(
        str(
            Fore.LIGHTBLACK_EX
            + "["
            + Fore.GREEN
            + "%(name)s"
            + Fore.LIGHTBLACK_EX
            + "]"
        ).expandtabs(10)
        + "["
        + Fore.BLUE
        + "%(levelname).1s"
        + Fore.LIGHTBLACK_EX
        + "] "
        + Style.RESET_ALL
        + "%(message)s"
    )
)


# alias for print()
def get_print_fn(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    return logger.info


print = get_print_fn("octogon")


# location of .scss files
STYLE_PATH = os.path.join(cwd, "style/")

# location of jinja2 templates
TEMPLATE_PATH = os.path.join(cwd, "templates/")

# location of scoreboard data
# SB_DATA_PATH = "output/sb_data.json"
SB_DATA_PATH = os.path.join(cwd, "output/sb_data_new.json")
