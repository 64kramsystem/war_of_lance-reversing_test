# Git — agent rules

## Branches and worktrees

- Use a separate branch per experiment run; record its starting commit. Use an isolated worktree when concurrent runs need separate working files.
- Preserve failed attempts and measured history. Do not rebase or squash a recorded run; corrections become new commits.

## Commits and merges

- Never use conventional-commit prefixes (`feat/`, etc.) in commit titles or branch names.
- **Never word-wrap commit messages.**
- Commit at meaningful analysis or implementation milestones. Keep evidence and the change it supports together.
- Check staged files for personal information and credentials before committing or pushing. Use repository-local commit identity settings without a private email address.

## Configuration

- Do not update `~/.gitconfig`.
