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
                Static("feat/init-git-commands", id="current-branch", classes="status-value"),
                classes="status-row"
            ),
            id="status-panel",
            classes="panel"
        )

    def on_mount(self) -> None:
        """Set up the status panel when mounted."""
        # Set the branch text with proper styling - green for clean status
        branch_label = self.query_one("#current-branch", Static)
        branch_text = Text("feat/init-git-commands")
        branch_text.stylize("green")
        branch_label.update(branch_text)

    def update_status(self, branch: str, status: str = "clean") -> None:
        """Update the status information.

        Args:
            branch: The name of the current branch
            status: Status string ('clean', 'modified', 'untracked')
        """
        branch_label = self.query_one("#current-branch", Static)
        branch_text = Text(branch)

        # Color based on status
        if status == "clean":
            branch_text.stylize("green")
        elif status == "modified":
            branch_text.stylize("red")
        elif status == "untracked":
            branch_text.stylize("magenta")

        branch_label.update(branch_text)
