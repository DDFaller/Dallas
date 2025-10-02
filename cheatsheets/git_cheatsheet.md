# Tiny Git Cheatsheet

## `git status`
Shows what’s changed, staged, or untracked.
```bash
git status
```

## `git add *`
Stages files matching the glob `*` (note: skips dotfiles).
```bash
git add *
```
**Safer alternatives:**
```bash
git add -A   # stage all changes (incl. deletions + dotfiles)
git add .    # stage changes in current dir
```

## `git commit -m "<message>"`
Records staged changes with a message.
```bash
git commit -m "Add homepage layout"
```

## `git push`
Sends local commits to the remote.
```bash
git push                # push to the tracked upstream
git push -u origin main # first push; sets upstream
```

## `git pull`
Updates your branch from the remote (fetch + merge).
```bash
git pull
# or keep history linear:
git pull --rebase
```

## `git fetch`
Downloads new commits/branches/tags **without** merging.
```bash
git fetch
git fetch --all --prune  # update all remotes, remove deleted refs
```

## `git clone`
Copies a remote repository to your machine.
```bash
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git
# optional custom folder:
git clone https://github.com/user/repo.git my-folder
```

---

## Quick workflow
```bash
git status
git add -A
git commit -m "Describe the change"
git push
```

## Update your local branch
```bash
git fetch
git pull --rebase
```
