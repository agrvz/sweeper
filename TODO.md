# TODO

## Features

- [x] Accept entrant and pick lists in txt file path form
- [x] Accept entrant and pick lists in CSV file path form
- [x] Output results to the terminal and to a file (CSV, txt, other?)
- [x] Argument to specify the output file name
- [x] Argument to limit draw to a certain number of entrants/picks
    - Not required - just limit entrants/picks in input files
- [x] Modes for handling imbalanced entrant count vs pick count in different ways
    - Not required - not clear what the use case is
- [ ] "Fancy" mode that shows loading bar, countdown, stylised terminal output etc
- [ ] "Plain" mode that simply shows the results, or writes the result file
- [x] Audit log to show inputs, outputs, and process
- [ ] Configurable to either choose picks or entrants in order, or neither
    - By default we pick in order of entrants, i.e. if entrants = ["a", "b", "c"], "a" will be allocated a pick first
- [x] Decide whether delay when drawing is configurable
    - Yes
- [ ] And whether delay should be artificial (draw has taken place immediately, only the printing of each round is delayed) or real (program genuinely waits for X seconds between draw rounds)
    - Refactor to draw entire result up front (and write audit log in real time too) - that way is safer, since if program is interrupted, the draw is not corrupted
- [x] Enforce uniqueness in picks and entrants
- [ ] Add option to allocate more than one pick per entrant (e.g. if there are 10 entrants, but 32 World Cup teams)
