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

### 🔹 Showing Specific Commits

To view detailed information about a specific commit, use `git show <commit>`, replacing `<commit>` with the commit hash. This will display changes made in the commit, along with the commit metadata.

```bash
bash
CopyEdit
git show <commit-hash>
```

## Viewing History for Specific Files

### 🔹 History of a Specific File

If you want to view the commit history for a specific file, use `git log <file>`. This will show all the commits that modified that particular file.

```bash
git log <file-name>
```

## Conclusion

Viewing the history in Git provides insight into how a project evolves over time. By using various log options and commands, you can easily track changes, identify contributors, and understand the development process.

Mastering these commands will allow you to navigate your project's history with ease and efficiency.