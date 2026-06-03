---
name: git-commit-push-ssd
description: Commit and push to external SSD
---

Create a full git commit with an appropriate message and push to external SSD (nevumo-git remote).

## Steps

1. Run `git status` to check current state
2. Run `git add .` to stage all changes
3. Run `git commit -m` with an appropriate commit message describing the changes
4. Run `git push nevumo-git main` to push to external SSD at `/Volumes/Transcend ESD310C 128GB/Nevumo_Git_Backups/Nevumo.git`
5. Report the commit hash and push status

## Important

- Always use descriptive commit messages that explain what was changed and why
- The external SSD remote is named `nevumo-git`
