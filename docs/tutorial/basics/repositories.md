# Repositories

```markdown

# 🗃️ Git Repositories: A Quick Guide

This guide explains essential repository operations in Git, including creating, connecting, cloning, and forking, along with a summary table of commands.

---

## 1️⃣ How to Create a Repository with `git init`

To start a new Git repository in your local project directory:

```bash
git init
```

This command creates a `.git/` folder that tracks all version history and enables Git operations.

✅ **Example:**

```bash
mkdir my-project
cd my-project
git init
```

---

## 2️⃣ How to Connect the Repository to a Global (Remote) Repository

Once your local repo is ready, connect it to a remote repository (e.g., on GitHub):

```bash
git remote add origin <remote-repo-url>
```

✅ **Example:**

```bash
git remote add origin https://github.com/username/my-repo.git
```

To push your code for the first time:

```bash
git push -u origin main
```

---

## 3️⃣ How to Clone a Repository

To copy a remote repository to your local machine:

```bash
git clone <remote-repo-url>
```

✅ **Example:**

```bash
git clone https://github.com/username/project.git
```

---

## 4️⃣ How to Fork a Repository

Forking a repository is done through platforms like GitHub:

1. Go to the repository page on GitHub.
2. Click the **Fork** button (top right corner).
3. This creates a copy of the repo under your GitHub account.

To work with the fork:

```bash
git clone https://github.com/your-username/forked-repo.git
```

---

## 6️⃣ Summary Table of Commands

| Command                            | Description                                         |
|------------------------------------|-----------------------------------------------------|
| `git init`                         | Initializes a new Git repository locally            |
| `git remote add origin <url>`     | Connects local repo to a remote repository          |
| `git push -u origin main`         | Pushes commits to the remote for the first time     |
| `git clone <url>`                 | Clones a remote repository to your local machine    |
| *(Forking is done via GitHub)*    | Fork a repo through the GitHub UI                   |

---
```
