import logging
import random
import sys
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
    draw_order: str = "entrants",
    delay: float = 1.0,
    quiet: bool = False,
    debug: bool = False,
) -> dict:
    """
    Map one pick to each entrant. Return a dictionary mapping entrants to picks.
    Does not modify original lists in place.

    Arguments:
        - entrants (list):  List of entrants (must be unique). entrants >= picks
                            must be true.
        - picks (list):     List of picks (must be unique)
        - draw_order (str): Draw in order of entrants list (i.e. 'entrant 1 gets...'),
                            picks list (i.e. 'pick 1 goes to...'), or shuffled (i.e.
                            shuffle entrants, then 'entrant 3 gets...').
                            Options: "entrants", "picks", "shuffle". Default is "entrant".
        - delay (float):    Delay in seconds between draws (default is 1.0)
        - quiet (bool):     If True, no terminal output is printed except the final result
        - debug (bool):     If True, picks are assigned in deterministic order (essentially
                            they are zipped together) instead of being chosen randomly.
                            Default is False.
    """
    logger.debug(f"Running draw with debug={debug}")
    logger.debug(f"({len(entrants)}) {entrants=}")
    logger.debug(f"({len(picks)}) {picks=}")
    logger.debug(f"{draw_order=}")
    logger.debug(f"{delay=}")
    logger.debug(f"{quiet=}")

    if len(set(entrants)) < len(entrants):
        message = f"Entrants must be unique but found duplicates: {entrants}"
        logger.error(message)
        raise ValueError(message)

    if len(set(picks)) < len(picks):
        message = f"Picks must be unique but found duplicates: {picks}"
        logger.error(message)
        raise ValueError(message)

    if len(picks) < len(entrants):
        message = f"There are not enough picks ({len(picks)}) to give all entrants ({len(entrants)}) a pick"
        logger.error(message)
        raise ValueError(message)

    if draw_order not in ["entrants", "picks", "shuffle"]:
        message = f"draw_order must be one of 'entrants', 'picks', or 'shuffle', got {draw_order}"
        logger.error(message)
        raise ValueError(message)

    entrants_copy = deepcopy(entrants)
    picks_copy = deepcopy(picks)

    if draw_order == "shuffle":
        random.shuffle(entrants_copy)

    result = {}
    table = PrettyTable(["Entrant", "Pick"])

    # Draw in order of entrants
    if draw_order in ["entrants", "shuffle"]:
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
    # Draw in order of picks
    elif draw_order == "picks":
        for index, pick in enumerate(picks_copy):
            logger.debug(f"Drawing for pick {index + 1}: {pick}")
            if debug:
                # If debug mode is on, assign entrants in order
                entrant = entrants_copy[index]
            else:
                # Remove a random entrant from the list
                entrant = entrants_copy.pop(random.randint(0, len(entrants_copy) - 1))

            result[entrant] = pick
            logger.debug(f"Pick {pick} drawn by entrant {entrant}")
            table.add_row([entrant, pick])
    else:
        message = f"draw_order must be one of 'entrants', 'picks', or 'shuffle', got {draw_order}"
        logger.error(message)
        raise ValueError(message)

    undrawn_picks = [pick for pick in picks_copy if pick not in result.values()]
    logger.debug(f"Results table\n{table}")
    logger.debug(f"Undrawn picks ({len(undrawn_picks)}): {undrawn_picks}")
    logger.debug("Draw complete")

    if not quiet:
        # Print results to terminal
        if draw_order in ["entrants", "shuffle"]:
            for index, (entrant, pick) in enumerate(result.items()):
                print(f"Entrant {index + 1}: {entrant}")
                time.sleep(delay)
                print("\nDrawing...\n")
                time.sleep(delay)
                print(f"{entrant} ... draws ... {pick}\n")
                time.sleep(delay * 2)
                print("------------------------------------\n")
        elif draw_order == "picks":
            for index, (entrant, pick) in enumerate(result.items()):
                print(f"Pick {index + 1}: {pick}")
                time.sleep(delay)
                print("\nDrawing...\n")
                time.sleep(delay)
                print(f"{pick} ... drawn by ... {entrant}\n")
                time.sleep(delay * 2)
                print("------------------------------------\n")
        print(f"Undrawn picks ({len(undrawn_picks)}): {undrawn_picks}\n")
        time.sleep(delay)

    print("\nDraw complete.\n")
    print(f"Results:\n{table}")
    return result


examples = """EXAMPLES

Create and draw a sweepstake using text file inputs:

sweeper draw --picks picks.txt --entrants entrants.txt

Use CSV files for the inputs, specifying the column names to use:

sweeper draw --picks picks.csv --picks-column name --entrants entrants.csv --entrants-column name

Or use the column index:

sweeper draw --picks picks.csv --picks-column 1 --entrants entrants.csv --entrants-column 1

Write results to an output file:

sweeper draw --picks picks.txt --entrants entrants.txt --output-file results.csv

Draw in order of picks (i.e. 'pick 1 goes to...'):

sweeper draw --picks picks.txt --entrants entrants.txt --draw-order picks
"""

@click.command(epilog=examples)
@click.option(
    "--entrants",
    required=True,
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to file containing list of entrants",
)
@click.option(
    "--entrants-column",
    type=str,
    help="Column name or index to use from entrants file, if a CSV file",
)
@click.option(
    "--picks",
    required=True,
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to file containing list of picks",
)
@click.option(
    "--picks-column",
    type=str,
    help="Column name or index to use from picks file, if a CSV file",
)
@click.option(
    "--draw-order",
    type=click.Choice(["entrants", "picks", "shuffle"], case_sensitive=False),
    default="entrants",
    show_default=True,
    help="Order to draw picks in. "
    "Draw in order of entrants list ('entrant 1 gets...'), "
    "picks list ('pick 1 goes to...'), "
    "or in order of entrants, but shuffled ('entrant 3 gets...')",
)
@click.option(
    "--delay",
    default=1.0,
    show_default=True,
    type=float,
    help="Delay between draw rounds in seconds",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="If set, no terminal output is printed except the final result",
)
@click.option(
    "--output-file",
    type=click.Path(exists=False, writable=True, dir_okay=False),
    help="File path to write results to. CSV or JSON supported. "
    "If not passed, results are printed to terminal and no file is written",
)
def draw_command(
    *,
    entrants: Path,
    entrants_column: str | int | None = None,
    picks: Path,
    picks_column: str | int | None = None,
    draw_order: str = "entrants",
    delay: float = 1.0,
    quiet: bool = False,
    output_file: Path | None = None,
) -> dict:
    """
    Start a sweepstake draw. Allocate one pick per entrant.
    """
    logger.debug("START: Running draw")
    logger.debug(f"Running command: {sys.argv[1:]}")

    picks = Path(picks)
    entrants = Path(entrants)
    if output_file:
        output_file = Path(output_file)

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

    logger.debug("Calling draw function")
    results = draw(
        entrants=entrants_list,
        picks=picks_list,
        draw_order=draw_order,
        delay=delay,
        quiet=quiet,
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
