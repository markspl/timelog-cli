# timelog-cli

Simple time/task logging on the command line. Plain-text log, no dependencies.

- Log when you **start** a task
- The duration of a task is the time until the next entry
- Show current running task or all tasks and totals
- Add notes if needed (planned)

## Commands

```bash
tl add <description>            # start a task now

# Planned commands, in no particular order
tl list                         # list of entries and totals
tl note <one-line note>         # add a note to the current task
tl now                          # show current task and duration
tl edit                         # open today's log file in $EDITOR
tl stop [reason]                # end the current task (e.g. lunch, or going home). Reason is optional.
tl help                         # overview of all commands
tl version                      # show the version
tl delete                       # delete today's log file
tl nonwork [add|remove|edit]    # non-work tasks whose time is not counted
```

If the text contains special characters, put it in quotes: `tl note "it's done"`.

## Installation

Requires Python 3.8 or newer and git. No other dependencies.

**1. Clone the project.** Pick a folder where it can stay:

```bash
git clone git@github.com:markspl/timelog-cli.git
cd timelog-cli
```

**2. Check that the name `tl` is free.** If this prints nothing, it is free:

```bash
type -a tl
```

> If you plan to use another name, go for it! E.g. `type -a wdid` (What Did I Do?)

**3. Add an alias** that points to the script. Run the line for your shell from inside the `timelog-cli` folder:

```bash
# Bash
echo "alias tl='python3 $(pwd)/tl.py'" >> ~/.bashrc

# or Zsh
echo "alias tl='python3 $(pwd)/tl.py'" >> ~/.zshrc
```

> Use `>>` (append). A single `>` would overwrite your whole shell config (been there, done that).

> If you chose another name, replace `alias tl=` with e.g. `alias wdid=`.

**4. Reload the shell config**, or just open a new terminal:

```bash
source ~/.bashrc    # Bash, or
source ~/.zshrc     # Zsh
```

Try it with `tl list`.

## Design ideas

- A task lasts from its own `add` line to the next `add` or `stop` line.
- `stop` ends the current task. The time after it is not counted, and it has an optional reason, e.g. `tl stop lunch`.
- `note` adds a line to the current task. It does not end the task and does not change the totals.
- Each day has its own file, and a new day starts with nothing running.
- Totals group by exact task name.

## Log file

Data lives in one plain-text file per day: `~/.timelog/<yyyy-mm-dd>.tsv`

One line per entry, with three tab-separated fields: date and time, type (`add`, `note` or `stop`), and text. The text of a `stop` is optional.

```text
2026-09-23 08:30	add	Ticket-67: Investigate
2026-09-23 09:15	add	Team daily
2026-09-23 09:30	add	Ticket-67: Investigate
2026-09-23 11:00	stop	lunch
2026-09-23 12:00	add	Alert-123
2026-09-23 12:20	note	Noticed an issue with logging, created ticket Ticket-69
2026-09-23 14:00	add	coffee
2026-09-23 14:30	add	Ticket-68
2026-09-23 16:00	stop
```

The file is append-only, and you can open and edit it with any editor. Durations are not stored. They are calculated from the times whenever you list, so fixing a wrong time fixes every total.

## Usage

> This example includes planned commands.

```console
$ tl add Ticket-67: Investigate
Started: Ticket-67: Investigate (08:30)

$ tl add Team daily
Started: Team daily (09:15)

$ tl now
Team daily (15m)

# Team daily has not ended yet, so it is marked (running)
$ tl list
Wed 2026-09-23

08:30      45m  Ticket-67: Investigate
09:15      15m  Team daily (running)

Totals
Ticket-67: Investigate      45m
Team daily                  15m (running)

Work total: 1h 00m

$ tl add Ticket-67: Investigate
Started: Ticket-67: Investigate (09:30)

$ tl stop lunch
Stopped: lunch (11:00)

$ tl add Alert-123
Started: Alert-123 (12:00)

$ tl note Noticed an issue with logging, created ticket Ticket-69
Note added.

$ tl add coffee
Started: coffee (14:00)

$ tl add Ticket-68
Started: Ticket-68 (14:30)

$ tl stop
Stopped (16:00)

$ tl list
Wed 2026-09-23

08:30      45m  Ticket-67: Investigate
09:15      15m  Team daily
09:30   1h 30m  Ticket-67: Investigate
11:00       --  stop: lunch
12:00   2h 00m  Alert-123
12:20           > Noticed an issue with logging, created ticket Ticket-69
14:00      30m  coffee
14:30   1h 30m  Ticket-68
16:00       --  stop

Totals
Ticket-67: Investigate   2h 15m
Alert-123                2h 00m
Ticket-68                1h 30m
Team daily                  15m
coffee                      30m

Work total: 6h 30m
```

License: [MIT](LICENSE)
