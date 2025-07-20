import random
import time
from pathlib import Path

import click
from prettytable import PrettyTable

from sweeper.io import get_lines_from_file, load_csv


@click.command()
@click.option("--teams", type=str, help="Path to file containing list of teams")
@click.option(
    "--teams-column",
    type=str,
    help="Column name or index for teams file, if a CSV file",
)
@click.option(
    "--participants", type=str, help="Path to file containing list of participants"
)
@click.option(
    "--participants-column",
    type=str,
    help="Column name or index for participants file, if a CSV file",
)
@click.option(
    "--delay", default=1, type=float, help="Delay between draw rounds in seconds"
)
def draw(
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
            teams_list = load_csv(filepath=teams, column_index=teams_column)
        except ValueError:
            teams_list = load_csv(filepath=teams, column_name=teams_column)

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

    if teams.suffix == ".txt":
        teams_list = get_lines_from_file(filepath=teams)
        participants_list = get_lines_from_file(filepath=participants)

    if len(teams_list) < len(participants_list):
        print("There are not enough teams to give every participant a team.")
        return None
    else:
        result = {}
        for index, participant in enumerate(participants_list):
            # Remove a random team from the list
            team = teams_list.pop(random.randint(0, len(teams_list) - 1))
            result[participant] = team
            print(f"Participant {index + 1}: {participant}")
            time.sleep(delay)
            print("\nDrawing...\n")
            time.sleep(delay)
            print(f"{participant} ... draws ... {team}\n")
            time.sleep(delay * 2)
            print("------------------------------------\n")

        print(f"Undrawn teams: {teams_list}\n")
        time.sleep(delay)

        table = PrettyTable(["Participant", "Team"])
        for key, val in result.items():
            table.add_row([key, val])
        table.sortby = "Participant"

        print(table)
        print("\nDraw complete.")
        return result


if __name__ == "__main__":
    draw(
        teams=Path("teams.csv"),
        teams_column="name",
        participants=Path("participants.csv"),
        participants_column="name",
        delay=0.1,
    )