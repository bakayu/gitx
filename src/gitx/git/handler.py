import os
import subprocess
# Remove or use Path
from typing import List, Dict, Optional, Tuple, Any


class GitHandler:
    """Handles Git operations."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize the Git handler.

        Args:
            repo_path: Path to the Git repository. Uses current directory if None.
        """
        self.repo_path = repo_path or os.getcwd()

        # Verify this is a git repository
        self._check_git_repository()

    def _check_git_repository(self) -> None:
        """Check if the current directory is a git repository."""
        try:
            self._run_git_command("rev-parse", "--is-inside-work-tree")
        except subprocess.CalledProcessError:
            # Fix f-string missing placeholder issue
            raise ValueError(f"The directory '{self.repo_path}' is not a Git repository")

    def _run_git_command(self, *args: str, capture_output: bool = True) -> subprocess.CompletedProcess:
        """Run a git command and return the result.

        Args:
            *args: Arguments to pass to git
            capture_output: Whether to capture the command output

        Returns:
            The completed process with output if capture_output is True
        """
        cmd = ["git", "-C", self.repo_path] + list(args)

        return subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=True
        )

    def get_status(self) -> Dict[str, List[str]]:
        """Get the status of the repository."""
        result = self._run_git_command("status", "--porcelain")

        status = {
            "untracked": [],
            "modified": [],
            "staged": [],
            "deleted": [],
            "renamed": []
        }

        for line in result.stdout.splitlines():
            if not line:
                continue

            # The first two characters represent the status
            code = line[:2]
            file_path = line[3:]

            # Parse the status code
            # M = modified, A = added, R = renamed, D = deleted, ?? = untracked
            if code == "??":
                status["untracked"].append(file_path)
            elif code[0] == "M" or code[1] == "M":
                if code[0] != " ":  # Changes in the staging area
                    status["staged"].append(file_path)
                if code[1] != " ":  # Changes in the working directory
                    status["modified"].append(file_path)
            elif code[0] == "A":
                status["staged"].append(file_path)
            elif code[0] == "D" or code[1] == "D":
                if code[0] != " ":  # Deleted in the staging area
                    status["staged"].append(file_path)
                if code[1] != " ":  # Deleted in the working directory
                    status["deleted"].append(file_path)
            elif code[0] == "R":
                status["renamed"].append(file_path)

        return status

    def get_branches(self) -> List[Dict[str, Any]]:
        """Get all branches in the repository."""
        # Get local branches
        result = self._run_git_command("branch", "--format=%(refname:short)")
        local_branches = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        # Get current branch
        try:
            current_branch = self.get_current_branch()
        except subprocess.CalledProcessError:
            current_branch = "HEAD detached"

        # Get remote branches
        result = self._run_git_command("branch", "-r", "--format=%(refname:short)")
        remote_branches = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        branches = []
        for branch in local_branches:
            remote = None
            # Find the corresponding remote branch if it exists
            for remote_branch in remote_branches:
                if remote_branch.endswith("/" + branch):
                    remote = remote_branch
                    break

            branches.append({
                "name": branch,
                "current": branch == current_branch,
                "remote": remote
            })

        return branches

    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        result = self._run_git_command("rev-parse", "--abbrev-ref", "HEAD")
        return result.stdout.strip()

    def get_commit_history(self, count: int = 20) -> List[Dict[str, str]]:
        """Get commit history.

        Args:
            count: Number of commits to retrieve

        Returns:
            List of commit dictionaries with hash, author, date, and message
        """
        # Format: hash, author name, author email, date, subject
        format_str = "--pretty=format:%h|%an|%ae|%ar|%s"
        result = self._run_git_command("log", "-n", str(count), format_str)

        commits = []
        for line in result.stdout.splitlines():
            if not line:
                continue

            parts = line.split("|")
            if len(parts) >= 5:
                commits.append({
                    "hash": parts[0],
                    "author": f"{parts[1]} <{parts[2]}>",
                    "date": parts[3],
                    "message": parts[4]
                })

        return commits

    def get_commit_details(self, commit_hash: str) -> Dict[str, Any]:
        """Get detailed information about a specific commit.

        Args:
            commit_hash: The commit hash to get details for

        Returns:
            Dictionary with commit details including full hash, author, date, message, and changed files
        """
        # Get basic commit info
        format_str = "--pretty=format:%H|%an|%ae|%ad|%s"
        result = self._run_git_command("show", "--no-patch", format_str, commit_hash)

        parts = result.stdout.strip().split("|")
        if len(parts) < 5:
            return {}

        # Get changed files
        files_result = self._run_git_command("show", "--name-status", "--pretty=format:", commit_hash)

        changed_files = {
            "added": [],
            "modified": [],
            "deleted": []
        }

        for line in files_result.stdout.splitlines():
            if not line.strip():
                continue

            parts_file = line.split()
            if len(parts_file) >= 2:
                status, file_path = parts_file[0], " ".join(parts_file[1:])

                if status == "A":
                    changed_files["added"].append(file_path)
                elif status == "M":
                    changed_files["modified"].append(file_path)
                elif status == "D":
                    changed_files["deleted"].append(file_path)

        return {
            "hash": parts[0],
            "author": f"{parts[1]} <{parts[2]}>",
            "date": parts[3],
            "message": parts[4],
            "changed_files": changed_files
        }

    def get_repo_status_summary(self) -> Dict[str, str]:
        """Get a summary of the repository status."""
        status = self.get_status()
        current_branch = self.get_current_branch()

        # Check if working directory is clean
        is_clean = not (status["modified"] or status["untracked"] or status["deleted"])
        status_text = "✓ clean" if is_clean else "! modified"

        # Get ahead/behind info
        try:
            ahead_behind = self._run_git_command(
                "rev-list", "--left-right", "--count", "@{u}...HEAD"
            )
            behind, ahead = ahead_behind.stdout.strip().split()
            remote_status = f"origin (ahead:{ahead}, behind:{behind})"
        except (subprocess.CalledProcessError, ValueError):
            remote_status = "no upstream branch"

        return {
            "branch": current_branch,
            "status": status_text,
            "remote": remote_status
        }

    def get_file_diff(self, file_path: str, staged: bool = False) -> str:
        """Get the diff for a specific file.

        Args:
            file_path: Path to the file
            staged: Whether to get the staged diff

        Returns:
            Diff output as a string
        """
        args = ["diff", "--color=never"]

        if staged:
            args.append("--staged")

        args.append("--")
        args.append(file_path)

        result = self._run_git_command(*args)
        return result.stdout

    def stage_file(self, file_path: str) -> bool:
        """Stage a file.

        Args:
            file_path: Path to the file to stage

        Returns:
            True if successful
        """
        try:
            self._run_git_command("add", "--", file_path, capture_output=False)
            return True
        except subprocess.CalledProcessError:
            return False

    def unstage_file(self, file_path: str) -> bool:
        """Unstage a file.

        Args:
            file_path: Path to the file to unstage

        Returns:
            True if successful
        """
        try:
            self._run_git_command("reset", "HEAD", "--", file_path, capture_output=False)
            return True
        except subprocess.CalledProcessError:
            return False

    def commit(self, message: str) -> bool:
        """Commit staged changes.

        Args:
            message: Commit message

        Returns:
            True if successful
        """
        try:
            self._run_git_command("commit", "-m", message, capture_output=False)
            return True
        except subprocess.CalledProcessError:
            return False

    def checkout_branch(self, branch_name: str) -> bool:
        """Checkout a branch.

        Args:
            branch_name: Name of the branch to checkout

        Returns:
            True if successful
        """
        try:
            self._run_git_command("checkout", branch_name, capture_output=False)
            return True
        except subprocess.CalledProcessError:
            return False

    def create_branch(self, branch_name: str) -> bool:
        """Create a new branch.

        Args:
            branch_name: Name of the branch to create

        Returns:
            True if successful
        """
        try:
            self._run_git_command("checkout", "-b", branch_name, capture_output=False)
            return True
        except subprocess.CalledProcessError:
            return False

    def merge_branch(self, branch_name: str) -> Tuple[bool, Optional[str]]:
        """Merge a branch into the current branch.

        Args:
            branch_name: Name of the branch to merge

        Returns:
            Tuple of (success, error_message)
        """
        try:
            result = self._run_git_command("merge", branch_name)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def pull(self) -> Tuple[bool, Optional[str]]:
        """Pull changes from remote.

        Returns:
            Tuple of (success, output_or_error_message)
        """
        try:
            result = self._run_git_command("pull")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def push(self) -> Tuple[bool, Optional[str]]:
        """Push changes to remote.

        Returns:
            Tuple of (success, output_or_error_message)
        """
        try:
            result = self._run_git_command("push")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def execute_command(self, command: str) -> Tuple[bool, str]:
        """Execute a custom git command.

        Args:
            command: Git command to execute (without 'git' prefix)

        Returns:
            Tuple of (success, output_or_error_message)
        """
        try:
            # Split the command into arguments
            args = command.split()
            result = self._run_git_command(*args)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
