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


def draw(
    entrants: list,
    picks: list,
    delay: float = 1.0,
    plain: bool = False,
    debug: bool = False,
) -> dict:
    """
    Map one pick to each entrant. Return a dictionary mapping entrants to picks.
    Does not modify original lists in place.

    Arguments:
        - entrants (list): List of entrants (must be unique). entrants >= picks
                           must be true.
        - picks (list):    List of picks (must be unique)
        - delay (float):   Delay in seconds between draws (default is 1.0)
        - plain (bool):    If True, no terminal output is printed except the final result
        - debug (bool):    If True, picks are assigned in deterministic order (essentially
                           they are zipped together) instead of being chosen randomly.
                           Default is False.
    """
    logger.debug(f"Running draw with debug={debug}")
    logger.debug(f"({len(entrants)}) {entrants=}")
    logger.debug(f"({len(picks)}) {picks=}")
    logger.debug(f"{delay=}")

    if len(set(entrants)) < len(entrants):
        message = f"Entrants must be unique but found duplicates: {entrants}"
        logger.error(message)
        raise ValueError(message)

    if len(set(picks)) < len(picks):
        message = f"Picks must be unique but found duplicates: {picks}"
        logger.error(message)
        raise ValueError(message)

    if len(picks) < len(entrants):
        message = f"There are not enough picks ({len(picks)}) to give every entrant ({len(entrants)}) a pick"
        logger.error(message)
        raise ValueError(message)

    picks_copy = deepcopy(picks)
    entrants_copy = deepcopy(entrants)

    result = {}
    table = PrettyTable(["Entrant", "Pick"])
    for index, entrant in enumerate(entrants_copy):
        logger.debug(f"Drawing for entrant {index + 1}: {entrant}")
        if debug:
            # If debug mode is on, assign picks in order
            pick = picks_copy[index]
        else:
            # Remove a random pick from the list
            pick = picks_copy.pop(random.randint(0, len(picks_copy) - 1))

        result[entrant] = pick
        logger.debug(f"Assigned pick {pick} to entrant {entrant}")
        table.add_row([entrant, pick])

    table.sortby = "Entrant"
    logger.debug(f"Results table\n{table}")
    logger.debug(f"Undrawn picks ({len(picks_copy)}): {picks_copy}")
    logger.debug("Draw complete")

    if not plain:
        # Print results to terminal
        for index, (entrant, pick) in enumerate(result.items()):
            print(f"Entrant {index + 1}: {entrant}")
            time.sleep(delay)
            print("\nDrawing...\n")
            time.sleep(delay)
            print(f"{entrant} ... draws ... {pick}\n")
            time.sleep(delay * 2)
            print("------------------------------------\n")

        print(f"Undrawn picks ({len(picks_copy)}): {picks_copy}\n")
        time.sleep(delay)

    print("\nDraw complete.\n")
    print(f"Results:\n{table}")
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
    "--delay",
    default=1,
    type=float,
    help="Delay between draw rounds in seconds. Default is 1.0",
)
@click.option(
    "--plain",
    is_flag=True,
    default=False,
    help="If set, no terminal output is printed except the final result",
)
@click.option(
    "--output-file",
    type=click.Path(exists=False, writable=True, dir_okay=False),
    help="File path to write results to. CSV or JSON supported. If not passed, results are printed to terminal and no file is written",
)
def draw_command(
    *,
    picks: Path,
    picks_column: str | int,
    entrants: Path,
    entrants_column: str | int,
    delay: float,
    plain: bool = False,
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
            logger.debug(f"entrants_column is an integer - loading csv by column index")
            entrants_list = load_csv(filepath=entrants, column_index=entrants_column)
        except ValueError:
            logger.debug(f"entrants_column is a string - loading csv by column name")
            entrants_list = load_csv(filepath=entrants, column_name=entrants_column)
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
        plain=plain,
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
