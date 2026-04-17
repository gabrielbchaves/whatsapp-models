---
name: commit
description: Stage changes, bump version, update changelog, and commit. Handles three modes: main branch, feature branch without commit, feature branch with commit (amend).
disable-model-invocation: true
argument-hint: "[brief description of what changed]"
---

# Commit Skill

Commit the current changes following this project's release workflow.

## Step 1 — Read current state (run in parallel)

- `git status` — what's staged/unstaged
- `git branch --show-current` — current branch
- `git rev-list --count main..HEAD` — number of commits ahead of main (0 = none)
- Read `pyproject.toml` — current version
- Read `CHANGELOG.md` — top of file to understand the format

## Step 2 — Ensure pre-commit hooks are installed

Run `uv run pre-commit install` before committing so ruff (and any other hooks) run automatically on commit.
If `uv` or `pre-commit` is not available, skip this step and note it to the user.

## Step 3 — Determine mode

### Mode A — on `main`
Conditions: current branch is `main`

1. Infer a branch name from `$ARGUMENTS` or the diff (e.g. `feat/add-sequence-types`)
2. `git checkout -b <branch-name>`
3. Bump the **patch** version in `pyproject.toml`
4. Prepend a new entry to `CHANGELOG.md`
5. `git add -A`
6. Create a new commit (see format below)

### Mode B — on a feature branch, no commits ahead of main yet
Conditions: branch is not `main` AND `git rev-list --count main..HEAD` == 0

1. Bump the **patch** version in `pyproject.toml`
2. Prepend a new entry to `CHANGELOG.md`
3. `git add -A`
4. Create a new commit (see format below)

### Mode C — on a feature branch, already has commits ahead of main
Conditions: branch is not `main` AND `git rev-list --count main..HEAD` >= 1

1. `git add -A`
2. `git commit --amend --no-edit`
3. No version bump, no changelog edit

---

## Commit message format (Modes A and B)

```
<type>: <one-line summary of the change>

- <bullet 1>
- <bullet 2>
...
```

Rules:
- First line: conventional commit prefix (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`, etc.), imperative mood, max 72 chars total, no trailing period
- Blank line between summary and bullets
- Bullets mirror the changelog entry exactly
- No "Co-Authored-By" trailer

## CHANGELOG.md entry format

Match the existing format in the file. Typical structure:

```markdown
## v<new-version>

### Added / Changed / Fixed

- <bullet describing each meaningful change>
```

---

## Examples

### Example 1 — Mode A (on main)

Argument: `replace list with Sequence for covariance`

```
# ensure hooks
uv run pre-commit install

git checkout -b feat/sequence-types

# pyproject.toml: 0.2.0 → 0.2.1

# CHANGELOG.md prepended:
## v0.2.1

### Changed

- Replace `list[...]` with `Sequence[...]` on all Pydantic model fields for covariance and immutability

git add -A
git commit -m "refactor: replace list with Sequence for covariance

- Replace \`list[...]\` with \`Sequence[...]\` on all Pydantic model fields for covariance and immutability"
```

---

### Example 2 — Mode B (feature branch, no commits yet)

Branch `feat/template-parameter-name`, zero commits ahead of main.
Argument: `add parameter_name to template send parameters`

```
# ensure hooks
uv run pre-commit install

# pyproject.toml: 0.2.1 → 0.2.2

# CHANGELOG.md prepended:
## v0.2.2

### Added

- `parameter_name` optional field on `TextParameter`, `CurrencyParameter`, `DateTimeParameter`, `DocumentParameter`, `ImageParameter`, `VideoParameter`

git add -A
git commit -m "feat: add parameter_name to template send parameters

- \`parameter_name\` optional field on \`TextParameter\`, \`CurrencyParameter\`, \`DateTimeParameter\`, \`DocumentParameter\`, \`ImageParameter\`, \`VideoParameter\`"
```

---

### Example 3 — Mode C (feature branch, already has a commit)

Branch `feat/sequence-types`, 1 commit ahead of main.
A test was added after the initial commit.

```
# ensure hooks
uv run pre-commit install

git add -A
git commit --amend --no-edit
# no version bump, no changelog edit, no new commit
```

---

## Notes

- If `$ARGUMENTS` is empty, infer a description from `git diff --stat HEAD`
- Never use `--no-verify`
- Never add Co-Authored-By trailers
- Always read the top of `CHANGELOG.md` before writing to match the existing style exactly
