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


def draw(participants: list, teams: list, delay: float = 1.0) -> dict:
    """
    Draw a random team for each participant and return a dictionary mapping
    participants to teams. Does not modify original lists in place.
    """
    logger.debug("Running draw")
    logger.debug(f"({len(participants)}) {participants=}")
    logger.debug(f"({len(teams)}) {teams=}")
    logger.debug(f"{delay=}")

    result = {}
    if len(teams) < len(participants):
        message = f"There are not enough teams to give every participant a team"
        logger.error(message)
        raise ValueError(message)

    teams_copy = deepcopy(teams)
    participants_copy = deepcopy(participants)

    for index, participant in enumerate(participants_copy):
        logger.debug(f"Drawing for participant {index + 1}: {participant}")
        # Remove a random team from the list
        team = teams_copy.pop(random.randint(0, len(teams_copy) - 1))

        result[participant] = team
        logger.debug(f"Assigned team {team} to participant {participant}")
        print(f"Participant {index + 1}: {participant}")
        time.sleep(delay)
        print("\nDrawing...\n")
        time.sleep(delay)
        print(f"{participant} ... draws ... {team}\n")
        time.sleep(delay * 2)
        print("------------------------------------\n")

    logger.debug(f"Undrawn teams ({len(teams_copy)}): {teams_copy}")
    print(f"Undrawn teams ({len(teams_copy)}): {teams_copy}\n")
    time.sleep(delay)

    table = PrettyTable(["Participant", "Team"])
    for key, val in result.items():
        table.add_row([key, val])
    table.sortby = "Participant"

    logger.debug(f"Results table\n{table}")
    print(table)
    logger.debug("Draw complete")
    print("\nDraw complete.\n")
    return result


@click.command()
@click.option(
    "--teams",
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to file containing list of teams",
)
@click.option(
    "--teams-column",
    type=str,
    help="Column name or index to use from teams file, if a CSV file",
)
@click.option(
    "--participants",
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to file containing list of participants",
)
@click.option(
    "--participants-column",
    type=str,
    help="Column name or index to use from participants file, if a CSV file",
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
    teams: Path,
    teams_column: str | int,
    participants: Path,
    participants_column: str | int,
    delay: float,
    output_file: Path,
) -> dict:
    """
    Start a sweepstake draw. Allocate one team per participant.
    """

    logger.debug("START: Running draw")
    logger.debug(f"{teams=}")
    logger.debug(f"{teams_column=}")
    logger.debug(f"{participants=}")
    logger.debug(f"{participants_column=}")
    logger.debug(f"{delay=}")
    logger.debug(f"{output_file=}")

    teams = Path(teams)
    participants = Path(participants)
    if output_file:
        output_file = Path(output_file)

    if teams.suffix == ".csv":
        logger.debug(f"Teams file suffix is .csv")
        try:
            int(teams_column)
            logger.debug(f"teams_column is an integer - loading csv by column index")
            teams_list = load_csv(filepath=teams, column_index=int(teams_column))
        except ValueError:
            logger.debug(f"teams_column is a string - loading csv by column name")
            teams_list = load_csv(filepath=teams, column_name=teams_column)
    elif teams.suffix == ".txt":
        logger.debug(f"Teams file suffix is .txt")
        teams_list = get_lines_from_file(filepath=teams)
    else:
        logger.error(f"Teams file must be a .csv or .txt file, got {teams.suffix}")
        raise ValueError(f"Teams file must be a .csv or .txt file, got {teams.suffix}")

    if participants.suffix == ".csv":
        try:
            logger.debug(f"Participants file suffix is .csv")
            int(participants_column)
            logger.debug(
                f"participants_column is an integer - loading csv by column index"
            )
            participants_list = load_csv(
                filepath=participants, column_index=participants_column
            )
        except ValueError:
            logger.debug(
                f"participants_column is a string - loading csv by column name"
            )
            participants_list = load_csv(
                filepath=participants, column_name=participants_column
            )
    elif participants.suffix == ".txt":
        logger.debug(f"Participants file suffix is .txt")
        participants_list = get_lines_from_file(filepath=participants)
    else:
        logger.error(
            f"Participants file must be a .csv or .txt file, got {participants.suffix}"
        )
        raise ValueError(
            f"Participants file must be a .csv or .txt file, got {participants.suffix}"
        )

    logger.debug("Calling draw function")
    results = draw(
        participants=participants_list,
        teams=teams_list,
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
