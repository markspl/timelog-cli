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

**2. Write the release notes.** They are the commit titles since the previous release tag. Do this before the version bump, so the release commit is not in the list:

```bash
PREV=$(git describe --tags --abbrev=0)   # the previous release tag, e.g. v0.0.1
VERSION=v0.1.0                           # the new version
echo "$PREV -> $VERSION"
echo "### What's Changed" > notes.md
git log "$PREV"..HEAD --no-merges --pretty=format:"* %s" >> notes.md
echo >> notes.md
cat notes.md
```

> Keep these as separate commands. In the VS Code terminal, wrapping them in `{ ...; } > notes.md` writes hidden terminal codes into the file.

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
