# Commiting Changes

# Committing Changes in Git

## Overview

In Git, **committing changes** is the process of saving a snapshot of your project history. Before committing, files go through different stages. Understanding these stages is key to using Git effectively.

---

## File Stages in Git

Git tracks the state of every file in your project. These states define how Git sees each file before committing:

### 🔹 Untracked Files

These are new files in your working directory that Git doesn't know about yet.

- **Not being tracked** by Git
- Will not be part of any commit until added

---

- These files are ready to be committed

---

### 🔹 Committed Changes

Once files are staged, you can commit them to the repository history, creating a snapshot of the changes.

---

## Summary of Commands

| Action | Command |
| --- | --- |
| Check file status | `git status` |
| Add new/modified file to staging | `git add <file>` |
| Unstage a file | `git restore --staged <file>` |
| Commit staged changes | `git commit -m "message"` |

---

## Conclusion

Committing in Git isn’t just a single step—it’s the final stage in a flow that moves files from **untracked → unstaged → staged → committed**. Mastering this flow is essential for effective version control.