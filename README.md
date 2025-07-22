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

Or, to run without needing `uv run`, activate the virtual environment first:
```shell
source .venv/bin/activate
```

Then run `sweep` commands directly:
```shell
sweep --help
```

## Commands

### draw

Command to create and start a sweepstake draw. Allocates one pick per entrant. For example, picks might be countries in the World Cup, and entrants might be a list of friends' names.

View help for `draw` command:
```shell
uv run sweep draw --help
```

Run a sweepstake draw:
```shell
uv run sweep draw --picks picks.txt --entrants entrants.txt
```

## Developing

Run unit tests:
```shell
uv run pytest -v
```

Format code:
```shell
uv run ruff format .
```

## Examples

Create a sweepstake with entrants and picks using text file inputs, and start the draw:
```shell
uv run sweep draw --picks picks.txt --entrants entrants.txt --delay 1
```

When using CSV files for the inputs you must specify the column name to use:
```shell
uv run sweep draw --picks picks.csv --picks-column name --entrants entrants.csv --entrants-column name --delay 0.1
```

Or you can use the column index:
```shell
uv run sweep draw --picks picks.csv --picks-column 1 --entrants entrants.csv --entrants-column 1 --delay 0.1
```

Optionally specify an output file to write results to. Format can either be `.csv`. or `.json`:
```shell
uv run sweep draw --picks picks.csv --picks-column 1 --entrants entrants.csv --entrants-column 1 --delay 0.1 --output-file results.csv
```

## Auditing

Logs are written to `logs/audit.log` for auditing purposes. Parameters used to generate the sweepstake are logged, as is each drawn round.

Example:
```log
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - START: Running draw
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - picks='picks.txt'
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - picks_column=None
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - entrants='entrants.txt'
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - entrants_column=None
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - delay=0.0
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - output_file='output.csv'
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Picks file suffix is .txt
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Entrants file suffix is .txt
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Calling draw function
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Running draw
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - (3) entrants=['Harold', 'Jim', 'Margaret']
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - (3) picks=['Chiefs', 'Ravens', 'Bills']
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - delay=0.0
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Drawing for entrant 1: Harold
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Assigned pick Ravens to entrant Harold
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Drawing for entrant 2: Jim
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Assigned pick Bills to entrant Jim
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Drawing for entrant 3: Margaret
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Assigned pick Chiefs to entrant Margaret
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Undrawn picks (0): []
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Results table
+-------------+--------+
| Entrant |  Pick  |
+-------------+--------+
|    Harold   | Ravens |
|     Jim     | Bills  |
|   Margaret  | Chiefs |
+-------------+--------+
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Draw complete
2025-07-22 16:43:26 UTC - DEBUG    - sweeper.draw - Output file passed with .csv suffix - writing to file
```
