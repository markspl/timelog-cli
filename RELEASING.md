# Releasing

Everything is done in the terminal, manually, for now.

GitHub CLI (`gh`) is needed. Check with `gh auth status` that you are logged in.

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

**1. Change the version** in `timelog/__init__.py`, and check it:

```bash
tl version
```

**2. Create a release draft** to generate notes:

```bash
gh release create v0.1.0 --draft --title "v0.1.0" --generate-notes
```

**3. Save the draft notes to `CHANGELOG.md`:**

```bash
VERSION="v0.1.0"
DATE=$(date +%Y-%m-%d)
NOTES=$(gh release view "$VERSION" --json body --jq .body)
NEW_ENTRY=$(printf "## %s (%s)\n\n%s\n\n" "$VERSION" "$DATE" "$NOTES")
if [ -f CHANGELOG.md ]; then
  printf "%s\n%s" "$NEW_ENTRY" "$(cat CHANGELOG.md)" > CHANGELOG.md
else
  printf "# Changelog\n\n%s" "$NEW_ENTRY" > CHANGELOG.md
fi
```

**4. Commit both files and push:**

```bash
git add timelog/__init__.py CHANGELOG.md
git commit -m "Release 0.1.0"
git push
```

**5. Create the tag and push it:**

```bash
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
```

`git push` alone does not push tags.

**6. Publish the release:**

```bash
gh release edit v0.1.0 --draft=false
```

## Notes

- The generated notes list merged pull requests. Commits pushed straight to `main` are not listed, only a link that compares the two versions. Use pull requests with clear titles.
