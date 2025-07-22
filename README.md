# Sweeper

CLI for creating sweepstakes.

## Installation

Install dependencies:
```shell
uv sync
```

View `sweep` CLI help:
```shell
uv run sweep --help
```

Alternatively, to run without needing `uv run`, activate the virtual environment first:
```shell
source .venv/bin/activate
```

Then you can run `sweep` commands directly:
```shell
sweep --help
```


## Examples

Create a sweepstake with participants and teams using text file inputs, and start the draw:
```shell
uv run sweep draw --teams teams.txt --participants participants.txt --delay 1
```

When using CSV files for the inputs you must specify the column name to use:
```shell
uv run sweep draw --teams teams.csv --teams-column name --participants participants.csv --participants-column name --delay 0.1
```

Or you can use the column index:
```shell
uv run sweep draw --teams teams.csv --teams-column 1 --participants participants.csv --participants-column 1 --delay 0.1
```

Optionally specify an output file to write results to. Format can either be `.csv`. or `.json`:
```shell
uv run sweep draw --teams teams.csv --teams-column 1 --participants participants.csv --participants-column 1 --delay 0.1 --output-file results.csv
```

## Auditing

Logs are written to `logs/audit.log` for auditing purposes. Parameters used to generate the sweepstake are logged, as is each drawn round.

Example:
```log
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - START: Running draw
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - teams='teams.txt'
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - teams_column=None
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - participants='participants.txt'
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - participants_column=None
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - delay=0.0
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - output_file='output.csv'
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Teams file suffix is .txt
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Participants file suffix is .txt
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Calling draw function
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Running draw
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - (3) participants=['Harold', 'Jim', 'Margaret']
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - (3) teams=['Chiefs', 'Ravens', 'Bills']
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - delay=0.0
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Drawing for participant 1: Harold
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Assigned team Ravens to participant Harold
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Drawing for participant 2: Jim
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Assigned team Bills to participant Jim
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Drawing for participant 3: Margaret
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Assigned team Chiefs to participant Margaret
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Undrawn teams (0): []
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Results table
+-------------+--------+
| Participant |  Team  |
+-------------+--------+
|    Harold   | Ravens |
|     Jim     | Bills  |
|   Margaret  | Chiefs |
+-------------+--------+
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Draw complete
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Output file passed with .csv suffix - writing to file
```
