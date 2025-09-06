# Sweeper

CLI for creating sweepstakes.

---

## Installation

### Using pipx

```shell
pipx install git+https://github.com/agrvz/sweeper
```

### Using uv

```shell
uv tool install git+https://github.com/agrvz/sweeper
```

### Using pip

```shell
pip install git+https://github.com/agrvz/sweeper.git
```

### Validate installation

```shell
sweeper --help
```

---

## Using Sweeper

### Create and draw a sweepstake

Use the `draw` command to create and start a sweepstake draw. It allocates one pick per entrant. For example, picks might be a list of countries in the World Cup, and entrants might be a list of friends' names.

Create example files to hold entrants and picks:
```shell
echo "Harold\nJim\nMargaret" > entrants.txt
echo "Bills\nChiefs\nRavens" > picks.txt
```

Run a sweepstake draw:
```shell
sweeper draw --entrants entrants.txt --picks picks.txt
```

#### CLI reference

```
Usage: sweeper [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  draw  Start a sweepstake draw.
```

```
Usage: sweeper draw [OPTIONS]

  Start a sweepstake draw. Allocate one pick per entrant.

Options:
  -e, --entrants FILE             Path to file containing list of entrants
                                  [required]
  --entrants-column TEXT          Column name or index to use from entrants
                                  file, if a CSV file. Option required if
                                  get_path_suffix(--entrants) is '.csv'
  -p, --picks FILE                Path to file containing list of picks
                                  [required]
  --picks-column TEXT             Column name or index to use from picks file,
                                  if a CSV file. Option required if
                                  get_path_suffix(--picks) is '.csv'
  --draw-order [entrants|picks|shuffle]
                                  Order to draw picks in. Draw in order of
                                  entrants list ('entrant 1 gets...'), picks
                                  list ('pick 1 goes to...'), or in order of
                                  entrants, but shuffled ('entrant 3 gets...')
                                  [default: entrants]
  --delay FLOAT                   Delay between draw rounds in seconds
                                  [default: 1.0]
  -q, --quiet                     If set, no terminal output is printed except
                                  the final result
  --output-file FILE              File path to write results to. CSV or JSON
                                  supported. If not passed, results are
                                  printed to terminal and no file is written
  --help                          Show this message and exit.

  EXAMPLES

  Create and draw a sweepstake using text file inputs:

  sweeper draw --entrants entrants.txt --picks picks.txt

  Use CSV files for the inputs, specifying the column names to use:

  sweeper draw --entrants entrants.csv --entrants-column name --picks
  picks.csv --picks-column name

  Or use the column index:

  sweeper draw --entrants entrants.csv --entrants-column 1 --picks picks.csv
  --picks-column 1

  Write results to an output file:

  sweeper draw --entrants entrants.txt --picks picks.txt --output-file
  results.csv

  Draw in order of picks (i.e. 'pick 1 goes to...'):

  sweeper draw --entrants entrants.txt --picks picks.txt --draw-order picks
```

---

## Developing

Sweeper uses uv to manage dependencies.
```shell
uv sync --dev
```

Run unit tests:
```shell
uv run pytest -v
```

Format code with ruff:
```shell
uv run ruff format .
```

### CI

Opening a PR triggers workflows to validate code formatting and run unit tests.

---

## Auditing

Logs are written to `logs/audit.log` for auditing purposes. Arguments used to generate the sweepstake are logged and each round drawn is also logged.

Example:
```log
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - START: Running draw
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Running command: ['draw', '--picks', 'picks.txt', '--entrants', 'entrants.txt']
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Entrants file suffix is .txt
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Picks file suffix is .txt
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Calling draw function
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Running draw with debug=False
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - (3) entrants=['Harold', 'Jim', 'Margaret']
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - (3) picks=['Chiefs', 'Ravens', 'Bills']
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - draw_order='entrants'
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - delay=1.0
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - quiet=False
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Drawing for entrant 1: Harold
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Assigned pick Ravens to entrant Harold
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Drawing for entrant 2: Jim
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Assigned pick Chiefs to entrant Jim
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Drawing for entrant 3: Margaret
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Assigned pick Bills to entrant Margaret
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Results table
+----------+--------+
| Entrant  |  Pick  |
+----------+--------+
|  Harold  | Ravens |
|   Jim    | Chiefs |
| Margaret | Bills  |
+----------+--------+
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Undrawn picks (0): []
2025-07-30 22:45:05 UTC - DEBUG    - sweeper.draw - Draw complete
2025-07-30 22:45:18 UTC - DEBUG    - sweeper.draw - No output file specified - printing results
```
