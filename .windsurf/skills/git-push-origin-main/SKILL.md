---
name: git-push-origin-main
description: Commit and push to origin main and nevumo-git
---

Stage, commit, and push current changes to both origin main and nevumo-git.

## Steps

1. Run `git add .` to stage all changes
2. Run `git commit -m "описание"` with a descriptive commit message explaining the changes being pushed
3. Run `git push origin main` to push to the main branch on the origin remote
4. Run `git push nevumo-git main` to push to the external SSD remote
5. Report the commit hash and push status

## Important

- Always use descriptive commit messages that explain what was changed and why
- The external SSD remote is named `nevumo-git`
