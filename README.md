# Sweeper

CLI for creating sweepstakes.

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
