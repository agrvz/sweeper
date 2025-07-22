import logging
import random
import time
from copy import deepcopy
from pathlib import Path

import click
from prettytable import PrettyTable

from sweeper.io import (
    get_lines_from_file,
    load_csv,
    write_result_to_csv,
    write_result_to_json,
)


logger = logging.getLogger(__name__)


def draw(entrants: list, picks: list, delay: float = 1.0) -> dict:
    """
    Draw a random pick for each entrant and return a dictionary mapping
    entrants to picks. Does not modify original lists in place.
    """
    logger.debug("Running draw")
    logger.debug(f"({len(entrants)}) {entrants=}")
    logger.debug(f"({len(picks)}) {picks=}")
    logger.debug(f"{delay=}")

    result = {}
    if len(picks) < len(entrants):
        message = f"There are not enough picks to give every entrant a pick"
        logger.error(message)
        raise ValueError(message)

    picks_copy = deepcopy(picks)
    entrants_copy = deepcopy(entrants)

    for index, entrant in enumerate(entrants_copy):
        logger.debug(f"Drawing for entrant {index + 1}: {entrant}")
        # Remove a random pick from the list
        pick = picks_copy.pop(random.randint(0, len(picks_copy) - 1))

        result[entrant] = pick
        logger.debug(f"Assigned pick {pick} to entrant {entrant}")
        print(f"Entrant {index + 1}: {entrant}")
        time.sleep(delay)
        print("\nDrawing...\n")
        time.sleep(delay)
        print(f"{entrant} ... draws ... {pick}\n")
        time.sleep(delay * 2)
        print("------------------------------------\n")

    logger.debug(f"Undrawn picks ({len(picks_copy)}): {picks_copy}")
    print(f"Undrawn picks ({len(picks_copy)}): {picks_copy}\n")
    time.sleep(delay)

    table = PrettyTable(["Entrant", "Pick"])
    for key, val in result.items():
        table.add_row([key, val])
    table.sortby = "Entrant"

    logger.debug(f"Results table\n{table}")
    print(table)
    logger.debug("Draw complete")
    print("\nDraw complete.\n")
    return result


@click.command()
@click.option(
    "--picks",
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to file containing list of picks",
)
@click.option(
    "--picks-column",
    type=str,
    help="Column name or index to use from picks file, if a CSV file",
)
@click.option(
    "--entrants",
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to file containing list of entrants",
)
@click.option(
    "--entrants-column",
    type=str,
    help="Column name or index to use from entrants file, if a CSV file",
)
@click.option(
    "--delay", default=1, type=float, help="Delay between draw rounds in seconds"
)
@click.option(
    "--output-file",
    type=click.Path(exists=False, writable=True, dir_okay=False),
    help="File path to write results to. Either .csv or .json supported",
)
def draw_command(
    *,
    picks: Path,
    picks_column: str | int,
    entrants: Path,
    entrants_column: str | int,
    delay: float,
    output_file: Path,
) -> dict:
    """
    Start a sweepstake draw. Allocate one pick per entrant.
    """

    logger.debug("START: Running draw")
    logger.debug(f"{picks=}")
    logger.debug(f"{picks_column=}")
    logger.debug(f"{entrants=}")
    logger.debug(f"{entrants_column=}")
    logger.debug(f"{delay=}")
    logger.debug(f"{output_file=}")

    picks = Path(picks)
    entrants = Path(entrants)
    if output_file:
        output_file = Path(output_file)

    if picks.suffix == ".csv":
        logger.debug(f"Picks file suffix is .csv")
        try:
            int(picks_column)
            logger.debug(f"picks_column is an integer - loading csv by column index")
            picks_list = load_csv(filepath=picks, column_index=int(picks_column))
        except ValueError:
            logger.debug(f"picks_column is a string - loading csv by column name")
            picks_list = load_csv(filepath=picks, column_name=picks_column)
    elif picks.suffix == ".txt":
        logger.debug(f"Picks file suffix is .txt")
        picks_list = get_lines_from_file(filepath=picks)
    else:
        logger.error(f"Picks file must be a .csv or .txt file, got {picks.suffix}")
        raise ValueError(f"Picks file must be a .csv or .txt file, got {picks.suffix}")

    if entrants.suffix == ".csv":
        try:
            logger.debug(f"Entrants file suffix is .csv")
            int(entrants_column)
            logger.debug(
                f"entrants_column is an integer - loading csv by column index"
            )
            entrants_list = load_csv(
                filepath=entrants, column_index=entrants_column
            )
        except ValueError:
            logger.debug(
                f"entrants_column is a string - loading csv by column name"
            )
            entrants_list = load_csv(
                filepath=entrants, column_name=entrants_column
            )
    elif entrants.suffix == ".txt":
        logger.debug(f"Entrants file suffix is .txt")
        entrants_list = get_lines_from_file(filepath=entrants)
    else:
        logger.error(
            f"Entrants file must be a .csv or .txt file, got {entrants.suffix}"
        )
        raise ValueError(
            f"Entrants file must be a .csv or .txt file, got {entrants.suffix}"
        )

    logger.debug("Calling draw function")
    results = draw(
        entrants=entrants_list,
        picks=picks_list,
        delay=delay,
    )

    if output_file is None:
        logger.debug("No output file specified - printing results")
        return results
    elif output_file.suffix == ".csv":
        logger.debug(f"Output file passed with .csv suffix - writing to file")
        write_result_to_csv(result=results, path=output_file)
    elif output_file.suffix == ".json":
        logger.debug(f"Output file passed with .json suffix - writing to file")
        write_result_to_json(result=results, path=output_file)
    else:
        logger.error(
            f"Output file must be a .csv or .json file, got {output_file.suffix}"
        )
        raise ValueError(
            f"Output file must be a .csv or .json file, got {output_file.suffix}"
        )

    return None
