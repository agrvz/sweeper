import random
import time
from pathlib import Path

import click
from prettytable import PrettyTable

from sweeper.io import get_lines_from_file


@click.command()
@click.option("--teams", type=str, help="Path to file containing list of teams")
@click.option(
    "--participants", type=str, help="Path to file containing list of participants"
)
@click.option(
    "--delay", default=1, type=float, help="Delay between draw rounds in seconds"
)
def draw(*, teams: Path, participants: Path, delay: float) -> dict:
    """
    Start a sweepstake draw. Allocate one team per participant.
    """

    teams = get_lines_from_file(filepath=teams)
    participants = get_lines_from_file(filepath=participants)

    if len(teams) < len(participants):
        print("There are not enough teams to give every participant a team.")
        return None
    else:
        result = {}
        for index, participant in enumerate(participants):
            # Remove a random team from the list
            team = teams.pop(random.randint(0, len(teams) - 1))
            result[participant] = team
            print(f"Participant {index + 1}: {participant}")
            time.sleep(delay)
            print("\nDrawing...\n")
            time.sleep(delay)
            print(f"{participant} ... draws ... {team}\n")
            time.sleep(delay * 2)
            print("------------------------------------\n")

        print(f"Undrawn teams: {teams}\n")
        time.sleep(delay)

        table = PrettyTable(["Participant", "Team"])
        for key, val in result.items():
            table.add_row([key, val])
        table.sortby = "Participant"

        print(table)
        print("\nDraw complete.")
        return result
