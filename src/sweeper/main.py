import logging
import time
from pathlib import Path

import click

from sweeper.draw import draw_command


def setup_logging():
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)-8s - %(name)-12s - %(message)s"
    )
    formatter.converter = time.gmtime  # Use UTC time
    formatter.datefmt = "%Y-%m-%d %H:%M:%S UTC"

    path = Path("logs")
    path.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(filename=f"logs/audit.log")
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)


@click.group()
def sweeper():
    setup_logging()
    pass


sweeper.add_command(draw_command)


if __name__ == "__main__":
    sweeper()
