from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid
from textual.widgets import Header, Footer

from gitx.widgets.status_panel import StatusPanel
from gitx.widgets.file_tree import FileTree
from gitx.widgets.commit_log import CommitLog
from gitx.widgets.branches_panel import BranchesPanel
from gitx.widgets.command_panel import CommandPanel
from gitx.widgets.main_panel import MainPanel
from gitx.git.handler import GitHandler


class GitxApp(App):
    """A TUI Git client built with Textual."""

    CSS_PATH = "css/app.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit"),
        Binding(key="t", action="toggle_theme", description="Toggle theme"),
        Binding(key="s", action="stage_file", description="Stage file"),
        Binding(key="u", action="unstage_file", description="Unstage file"),
        Binding(key="c", action="commit", description="Commit"),
        Binding(key="p", action="push", description="Push"),
        Binding(key="f", action="pull", description="Pull (fetch)"),
        Binding(key="b", action="new_branch", description="New branch"),
        Binding(key="?", action="toggle_help", description="Help"),
        Binding(key="^p", action="palette", description="Command palette"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.git = GitHandler()

    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        yield Header(show_clock=True)

        # Left side - Status and Files
        yield Grid(
            # Left column - Status and file changes
            Container(
                StatusPanel(),
                FileTree(),
                BranchesPanel(),
                id="left-panels"
            ),

            # Right side - Main content area and logs
            Container(
                # Top right - Commit log
                CommitLog(),
                # Bottom right - Main content
                MainPanel(),
                id="right-panels"
            ),

            # Command panel at bottom
            Container(
                CommandPanel(),
                id="bottom-panel"
            ),

            id="app-layout"
        )

        yield Footer()

    def on_mount(self) -> None:
        """Initial setup when app is mounted."""
        self.title = "GitXApp"
        self.dark = True

        # Show welcome message in main panel
        main_panel = self.query_one(MainPanel)
        main_panel.show_welcome()

    def action_toggle_theme(self) -> None:
        """Toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_stage_file(self) -> None:
        """Stage the selected file."""
        self.notify("Action: Stage file (not implemented yet)")

    def action_unstage_file(self) -> None:
        """Unstage the selected file."""
        self.notify("Action: Unstage file (not implemented yet)")

    def action_commit(self) -> None:
        """Commit staged changes."""
        self.notify("Action: Commit (not implemented yet)")

    def action_push(self) -> None:
        """Push changes to remote."""
        self.notify("Action: Push (not implemented yet)")

    def action_pull(self) -> None:
        """Pull changes from remote."""
        self.notify("Action: Pull (not implemented yet)")

    def action_new_branch(self) -> None:
        """Create a new branch."""
        self.notify("Action: New branch (not implemented yet)")

    def action_toggle_help(self) -> None:
        """Toggle help screen."""
        self.notify("Action: Help (not implemented yet)")


def main() -> None:
    """Run the app."""
    app = GitxApp()
    app.run()


if __name__ == "__main__":
    main()
