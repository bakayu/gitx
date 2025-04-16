from textual.widgets import Static, RichLog
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label


class CommitLog(Static):
    """Widget to display commit history."""

    def compose(self) -> ComposeResult:
        """Compose the commit log."""
        yield Vertical(
            Label("[bold]2-Log[/bold]", classes="section-title"),
            RichLog(id="commit-log", wrap=False, highlight=True, markup=True),
            id="commit-log-panel",
            classes="panel"
        )

    def on_mount(self) -> None:
        """Set up the commit log when mounted."""
        self.refresh_log()

    def refresh_log(self, count: int = 20) -> None:
        """Refresh the commit log with the latest commits.

        Args:
            count: Number of commits to show
        """
        log = self.query_one(RichLog)
        log.clear()

        try:
            # Get actual commit history from git
            commits = self.app.git.get_commit_history(count)

            if not commits:
                log.write("[yellow]No commits found in this repository.[/yellow]")
                return

            # Get current branch for reference
            current_branch = self.app.git.get_current_branch()

            # Format and display the commits
            for i, commit in enumerate(commits):
                # Show branch indicator for the first commit
                branch_indicator = ""
                if i == 0:
                    branch_indicator = f"([red]HEAD → {current_branch}[/red])"

                # Display commit in a format similar to git log
                log.write(f"[green]✱[/green] [yellow]commit[/yellow] [green]{commit['hash']}[/green] {branch_indicator}")
                log.write(f"│ [blue]Author:[/blue] {commit['author']}")
                log.write(f"│ [blue]Date:[/blue]   {commit['date']}")
                log.write("│ ")

                # Format commit message with proper indentation
                for line in commit['message'].split("\n"):
                    log.write(f"│     {line}")

                log.write("│")
        except Exception as e:
            log.write(f"[red]Error loading commit history: {str(e)}[/red]")

    def on_click(self, event) -> None:
        """Handle click events to select commits."""
        # Find which line was clicked
        log = self.query_one(RichLog)

        try:
            # Get the line that was clicked
            line_index = log.get_line_at(event.y)
            if line_index is None:
                return

            line = log.get_content_at(line_index)

            # Check if this is a commit line (starts with ✱ commit)
            if "[green]✱[/green] [yellow]commit[/yellow]" in line:
                # Extract the commit hash
                parts = line.split()
                for i, part in enumerate(parts):
                    if "[green]" in part and len(part) > 15:  # Likely the hash
                        # Extract just the hash, removing formatting
                        commit_hash = part.replace("[green]", "").replace("[/green]", "")

                        # Show commit details in the main panel
                        main_panel = self.app.query_one('MainPanel')
                        main_panel.show_commit_details(commit_hash)
                        break
        except Exception:
            # Silently ignore any errors in click handling
            pass

    def update_log(self, count: int = 20) -> None:
        """Update the commit log with real commit data."""
        self.refresh_log(count)
