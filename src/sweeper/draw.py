import random
import time
from copy import deepcopy
from pathlib import Path

import click
from prettytable import PrettyTable

from sweeper.io import get_lines_from_file, load_csv


def draw(participants: list, teams: list, delay: float = 1.0) -> dict:
    """
    Draw a random team for each participant and return a dictionary mapping
    participants to teams. Does not modify original lists in place.
    """
    result = {}
    if len(teams) < len(participants):
        raise ValueError("There are not enough teams to give every participant a team.")

    teams_copy = deepcopy(teams)
    participants_copy = deepcopy(participants)

    for index, participant in enumerate(participants_copy):
        # Remove a random team from the list
        team = teams_copy.pop(random.randint(0, len(teams_copy) - 1))
        result[participant] = team
        print(f"Participant {index + 1}: {participant}")
        time.sleep(delay)
        print("\nDrawing...\n")
        time.sleep(delay)
        print(f"{participant} ... draws ... {team}\n")
        time.sleep(delay * 2)
        print("------------------------------------\n")

    print(f"Undrawn teams ({len(teams_copy)}): {teams_copy}\n")
    time.sleep(delay)

    table = PrettyTable(["Participant", "Team"])
    for key, val in result.items():
        table.add_row([key, val])
    table.sortby = "Participant"

    print(table)
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
    help="Column name or index for teams file, if a CSV file",
)
@click.option(
    "--participants",
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to file containing list of participants",
)
@click.option(
    "--participants-column",
    type=str,
    help="Column name or index for participants file, if a CSV file",
)
@click.option(
    "--delay", default=1, type=float, help="Delay between draw rounds in seconds"
)
def draw_command(
    *, teams: Path, teams_column, participants: Path, participants_column, delay: float
) -> dict:
    """
    Start a sweepstake draw. Allocate one team per participant.
    """

    teams = Path(teams)
    participants = Path(participants)

    if teams.suffix == ".csv":
        try:
            int(teams_column)
            teams_list = load_csv(filepath=teams, column_index=int(teams_column))
        except ValueError:
            teams_list = load_csv(filepath=teams, column_name=teams_column)
    elif teams.suffix == ".txt":
        teams_list = get_lines_from_file(filepath=teams)
    else:
        raise ValueError("Teams file must be a .csv or .txt file.")

    if participants.suffix == ".csv":
        try:
            int(participants_column)
            participants_list = load_csv(
                filepath=participants, column_index=participants_column
            )
        except ValueError:
            participants_list = load_csv(
                filepath=participants, column_name=participants_column
            )
    elif participants.suffix == "txt":
        participants_list = get_lines_from_file(filepath=participants)
    else:
        raise ValueError("Participants file must be a .csv or .txt file.")

    return draw(
        participants=participants_list,
        teams=teams_list,
        delay=delay,
    )
