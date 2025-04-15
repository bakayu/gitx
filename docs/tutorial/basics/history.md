# Viewing History

# Viewing History in Git

## Overview

Viewing the history of your project in Git allows you to track changes over time. Git keeps a detailed record of every commit made to the repository. You can explore this history using various commands, each showing different aspects of the commit history.

---

## Key Commands for Viewing History

Git provides several commands to view your repository's history. Here's a summary of the most common ones:

| Command | Description |
| --- | --- |
| `git log` | Displays the commit history. |
| `git log --oneline` | Shows a simplified log, one line per commit. |
| `git show <commit>` | Shows detailed information about a specific commit. |
| `git log <file>` | Shows the commit history for a specific file. |

---

## Viewing Commit History

### 🔹 Basic Log

The most commonly used command to view the history of commits is `git log`. It shows detailed information about each commit, including the commit hash, author, date, and commit message.

```bash
git log
```

### 🔹 Simplified Log

For a more concise view, `git log --oneline` shows each commit in a single line, displaying the commit hash and the commit message.

```bash
git log --oneline
```
