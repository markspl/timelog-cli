# Releasing

Everything is done in the terminal, manually, for now.

GitHub CLI (`gh`) is needed. Check with `gh auth status` that you are logged in.

The commands are for bash. On Windows, use Git Bash, not PowerShell.

The release notes are written once and used in two places: `CHANGELOG.md` and the GitHub release.

## Branches & Tags

- A release needs a tag, not a branch. Tags are made on `main`.
- Release branches (`release/0.1`) are only for patching an old version.
- Keep `main` always working using work branches (`feature/...`, `fix/...`).

## Version

The version looks like `0.1.0` (`MAJOR.MINOR.PATCH`). The tag has a `v` in front: `v0.1.0`.

- **Patch** (`0.1.0` → `0.1.1`): bug fixes
- **Minor** (`0.1.0` → `0.2.0`): new features
- **Major** (`0.9.0` → `1.0.0`): changes that break old use, e.g. old log files stop working

The version number is in one place: `timelog/__init__.py`.

## Steps

**1. Check that you are ready.** You should be on `main`, with a clean tree, up to date with origin:

```bash
git switch main
git pull
git status
```

**2. Write the release notes.** They are the commit titles since the previous release tag, grouped by type. Do this before the version bump, so the release commit is not in the list:

```bash
PREV=$(git describe --tags --abbrev=0)   # the previous release tag, e.g. v0.0.1
VERSION=v0.1.0                           # the new version
echo "$PREV -> $VERSION"

# section <title> <git log --grep options>: add one section, skipped if it has no commits
section() {
  local title=$1 lines
  shift
  lines=$(git log "$PREV"..HEAD --no-merges -E --pretty=format:"* %s" "$@")
  if [ -n "$lines" ]; then printf "### %s\n\n%s\n\n" "$title" "$lines" >> notes.md; fi
}
TYPE='(\(.+\))?!?:'   # optional scope and "!" after the type, e.g. fix(calc)!:

rm -f notes.md
section "⚠ Breaking changes" --grep='^[a-z]+(\(.+\))?!:' --grep='^BREAKING[ -]CHANGE:'
section "Features" --grep="^feat$TYPE"
section "Bug fixes" --grep="^fix$TYPE"
section "Performance improvements" --grep="^perf$TYPE"
section "Reverts" --grep="^revert$TYPE" --grep='^Revert "'
section "Other changes" --grep="^(docs|refactor|test|build|ci|style)$TYPE"
cat notes.md
```

> Keep the commands that write `notes.md` separate, as above. In the VS Code terminal, wrapping them in `{ ...; } > notes.md` writes hidden terminal codes into the file.

The sections follow the common conventional-changelog defaults, plus "Other changes" for internal work:

- **Breaking changes** lists commits marked with `!` (`feat!: new log format`) or with a `BREAKING CHANGE: <what breaks>` line in the commit body. They are also listed under their own type. A breaking change means a major version (see Version above).
- **Reverts** covers both `revert: ...` and the default `git revert` message (`Revert "..."`).
- `chore:` commits and commits without a type are left out. Check `git log "$PREV"..HEAD --oneline` if something seems missing.

Read `notes.md` and edit it if needed. It is used for both `CHANGELOG.md` and the GitHub release.

**3. Change the version** in `timelog/__init__.py`, and check that it matches `$VERSION`:

```bash
python tl.py version
```

**4. Add the notes to `CHANGELOG.md`**, newest entry first:

```bash
printf "## %s (%s)\n\n" "$VERSION" "$(date +%F)" > CHANGELOG.new
cat notes.md >> CHANGELOG.new
printf "\n" >> CHANGELOG.new
cat CHANGELOG.md >> CHANGELOG.new
mv CHANGELOG.new CHANGELOG.md
```

**5. Commit both files and push:**

```bash
git add timelog/__init__.py CHANGELOG.md
git commit -m "chore: release ${VERSION#v}"
git push
```

**6. Create the release.** This creates the tag on the release commit you just pushed, and uses the same notes:

```bash
gh release create "$VERSION" --target "$(git rev-parse HEAD)" --title "$VERSION" --notes-file notes.md
rm notes.md
```

To read the result on GitHub before it goes public, add `--draft` to the create command, then publish with `gh release edit "$VERSION" --draft=false`.

**7. Update your local tags:**

```bash
git fetch --tags
```

## Notes

- The notes come from commit titles, not pull requests, because GitHub's `--generate-notes` skips commits pushed straight to `main`. Clear titles (`feat:`, `fix:`, `refactor:`) make good notes.
- Pull requests are squash-merged, with the PR title as the commit title. Each PR then shows as one line in the notes, in the same style as direct commits. With a merge commit, every commit from the branch (including WIP ones) would be listed instead.
- Step 5 pushes straight to `main`. If `main` is later protected so that changes need a pull request, make the release commit on a branch, squash-merge it, and run step 6 after the merge.
- `gh release create` makes a lightweight tag. That is fine here, since the release page holds the message.
- Run the steps in one terminal session, since `PREV` and `VERSION` are shell variables.
