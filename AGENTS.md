# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this is

`tl` is a small command-line time logger written in pure Python (3.8+, standard library only). There is no build step, no linter config and no test suite yet. See [README.md](README.md) for the command list, the design rules (how durations work) and the log file format.

## Running

```bash
python tl.py add Some task          # entry point; same as the `tl` alias users set up
python tl.py add -t 14:30 Meeting
python tl.py note Something happened
python tl.py version
```

Commands write to the real data dir `~/.timelog/<yyyy-mm-dd>.tsv` (resolved with `Path.home()`). When trying things out, point the home directory at a temp folder first (`USERPROFILE` on Windows, `HOME` elsewhere) so you do not pollute the user's real log.

## Architecture

`tl.py` only parses the first argument and dispatches. Everything else is in the `timelog` package, in layers that must stay separate:

- `commands.py`: one function per command. It takes the argument list, returns the exit code, and wires the other modules together. Argument parsing and error printing (to stderr) live here.
- `model.py`: `Entry` dataclass (`time`, `type`, `text`) and its tab-separated line format (`to_line` / `from_line`). The text is normalized to a single line here.
- `storage.py`: the only module that touches the filesystem. One append-only file per day, named after the entry's own date.
- `render.py`: builds output strings. It never prints and never reads files; commands do the printing.
- `calc.py`: durations and totals. It is a stub (`NotImplementedError`) waiting for `tl list` / `tl now`.

Durations are never stored. They are derived from entry times when listing, so editing a time in the file fixes every total. A task lasts from its `add` until the next `add` or `stop`, and `note` entries do not end it. File order is not time order: `add -t` appends a backdated entry at the end of the file, so `calc.py` must sort entries by time before pairing them.

### Adding a command

1. Write the function in `commands.py`, using `render.py` for its messages.
2. Register it in `COMMANDS` in `tl.py` and remove it from the `PLANNED` set.
3. Add its type to `TYPES` in `model.py` if it writes a new entry type (`stop` is planned).
4. Update `USAGE` in `tl.py` and the command list in the README.

## Conventions

- PEP 8 style. `tl.py` was recently reformatted for this.
- Commit messages use conventional prefixes: `feat:`, `fix:`, `refactor:`.
- Pull requests are squash-merged, so the PR title becomes the commit title on `main` and a line in the release notes. Give PR titles the same prefixes.
- The version number lives only in `timelog/__init__.py`. Releases are manual and described in [RELEASING.md](RELEASING.md). `CHANGELOG.md` and the GitHub release share the same notes, built from commit titles.
