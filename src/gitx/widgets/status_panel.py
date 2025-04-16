from textual.widgets import Static
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Label
from rich.text import Text


class StatusPanel(Static):
    """Panel that shows the current status of the repository."""

    def compose(self) -> ComposeResult:
        """Compose the status panel."""
        yield Vertical(
            Label("[bold]1-Status[/bold]", classes="section-title"),
            Horizontal(
                Static("gitx ➜", classes="status-label"),
                Static("", id="current-branch", classes="status-value"),
                classes="status-row"
            ),
            id="status-panel",
            classes="panel"
        )

    def on_mount(self) -> None:
        """Set up the status panel when mounted."""
        self.refresh_status()

    def refresh_status(self) -> None:
        """Refresh the status information with current repository state."""
        try:
            # Get actual status from git
            status_info = self.app.git.get_repo_status_summary()

            branch_label = self.query_one("#current-branch", Static)
            branch_text = Text(f"{status_info['branch']} - {status_info['status']}")

            # Color based on status
            if "clean" in status_info["status"]:
                branch_text.stylize("green")
            elif "modified" in status_info["status"]:
                branch_text.stylize("red")
            elif "untracked" in status_info["status"]:
                branch_text.stylize("magenta")

            branch_label.update(branch_text)
        except Exception as e:
            branch_label = self.query_one("#current-branch", Static)
            error_text = Text(f"Error: {str(e)}")
            error_text.stylize("red")
            branch_label.update(error_text)

    def update_status(self, branch: str = None, status: str = None) -> None:
        """Update the status information manually.

        Args:
            branch: The name of the current branch (or None to auto-detect)
            status: Status string ('clean', 'modified', 'untracked', or None to auto-detect)
        """
        self.refresh_status()
