from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid
from textual.widgets import Header, Footer, Static, Input, Tree
from textual.screen import Screen

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
        Binding(key="r", action="refresh", description="Refresh"),
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

    def action_refresh(self) -> None:
        """Refresh all panels with the latest git data."""
        self.query_one(StatusPanel).refresh_status()
        self.query_one(FileTree).refresh_tree()
        self.query_one(CommitLog).refresh_log()
        self.query_one(BranchesPanel).refresh_branches()
        self.notify("Refreshed all panels")

    def action_toggle_theme(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def action_stage_file(self) -> None:
        """Stage the selected file."""
        file_tree = self.query_one(FileTree)
        tree = file_tree.query_one(Tree)

        if tree.cursor_node and hasattr(tree.cursor_node, 'data') and tree.cursor_node.data:
            file_path = tree.cursor_node.data.get("path")
            if file_path:
                if self.git.stage_file(file_path):
                    self.notify(f"Staged: {file_path}")
                    self.action_refresh()
                else:
                    self.notify(f"Failed to stage: {file_path}", severity="error")

    def action_unstage_file(self) -> None:
        """Unstage the selected file."""
        file_tree = self.query_one(FileTree)
        tree = file_tree.query_one(Tree)

        if tree.cursor_node and hasattr(tree.cursor_node, 'data') and tree.cursor_node.data:
            file_path = tree.cursor_node.data.get("path")
            if file_path:
                if self.git.unstage_file(file_path):
                    self.notify(f"Unstaged: {file_path}")
                    self.action_refresh()
                else:
                    self.notify(f"Failed to unstage: {file_path}", severity="error")

    def action_commit(self) -> None:
        """Commit staged changes."""
        # Create a modal input dialog for commit message
        from textual.widgets import Label  # Add this import

        class CommitScreen(Screen):
            def compose(self) -> ComposeResult:
                yield Container(
                    Label("[bold]Enter commit message:[/bold]"),
                    Input(id="commit-message", placeholder="Commit message..."),
                    Static("Press Enter to commit, Esc to cancel"),
                    id="commit-dialog"
                )

            def on_key(self, event):
                if event.key == "escape":
                    self.app.pop_screen()
                elif event.key == "enter":
                    commit_msg = self.query_one("#commit-message").value
                    if commit_msg.strip():
                        self.app.pop_screen()
                        if self.app.git.commit(commit_msg):
                            self.app.notify(f"Committed: {commit_msg}")
                            self.app.action_refresh()
                        else:
                            self.app.notify("Commit failed", severity="error")
                    else:
                        self.app.notify("Please enter a commit message", severity="warning")

        self.push_screen(CommitScreen())

    def action_push(self) -> None:
        """Push changes to remote."""
        success, output = self.git.push()
        if success:
            self.notify("Successfully pushed to remote")
        else:
            self.notify(f"Push failed: {output}", severity="error")
        self.action_refresh()

    def action_pull(self) -> None:
        """Pull changes from remote."""
        success, output = self.git.pull()
        if success:
            self.notify("Successfully pulled from remote")
        else:
            self.notify(f"Pull failed: {output}", severity="error")
        self.action_refresh()

    def action_new_branch(self) -> None:
        """Create a new branch."""
        # Create a modal input dialog for branch name
        from textual.widgets import Label  # Add this import

        class BranchScreen(Screen):
            def compose(self) -> ComposeResult:
                yield Container(
                    Label("[bold]Enter new branch name:[/bold]"),
                    Input(id="branch-name", placeholder="Branch name..."),
                    Static("Press Enter to create, Esc to cancel"),
                    id="branch-dialog"
                )

            def on_key(self, event):
                if event.key == "escape":
                    self.app.pop_screen()
                elif event.key == "enter":
                    branch_name = self.query_one("#branch-name").value
                    if branch_name.strip():
                        self.app.pop_screen()
                        if self.app.git.create_branch(branch_name):
                            self.app.notify(f"Created and switched to branch: {branch_name}")
                            self.app.action_refresh()
                        else:
                            self.app.notify(f"Failed to create branch: {branch_name}", severity="error")
                    else:
                        self.app.notify("Please enter a branch name", severity="warning")

        self.push_screen(BranchScreen())

    def action_toggle_help(self) -> None:
        """Toggle help screen."""
        from textual.widgets import Label  # Add this import

        class HelpScreen(Screen):
            def compose(self) -> ComposeResult:
                yield Container(
                    Label("[bold]GitX Help[/bold]"),
                    Static("[bold]Keyboard Shortcuts:[/bold]"),
                    Static("q - Quit"),
                    Static("t - Toggle theme"),
                    Static("s - Stage selected file"),
                    Static("u - Unstage selected file"),
                    Static("c - Commit staged changes"),
                    Static("p - Push to remote"),
                    Static("f - Pull from remote"),
                    Static("b - Create new branch"),
                    Static("r - Refresh all panels"),
                    Static("? - Toggle this help screen"),
                    Static("^p - Command palette"),
                    Static(""),
                    Static("Press any key to close this help"),
                    id="help-dialog"
                )

            def on_key(self, event):
                self.app.pop_screen()

        self.push_screen(HelpScreen())

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
