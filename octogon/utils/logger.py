import logging
from typing import Callable
from colorama import Fore, Style

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
def get_print_fn(name: str = "octogon") -> Callable:
    """Returns a logger function that is labled with the given name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    return logger.info
