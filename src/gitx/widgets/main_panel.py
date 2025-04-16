from textual.widgets import Static, RichLog
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label


class MainPanel(Static):
    """Main panel that changes based on context."""

    def compose(self) -> ComposeResult:
        """Compose the main panel."""
        yield Vertical(
            Label("[bold]4-Main[/bold]", classes="section-title"),
            RichLog(
                markup=True,
                highlight=True,
                id="main-content",
            ),
            id="main-panel",
            classes="panel"
        )

    def on_mount(self) -> None:
        """Set up the main panel when mounted."""
        content = self.query_one("#main-content", RichLog)
        content.clear()
        content.write("Select a file to view its contents or a commit to view its details.")

    def show_file_diff(self, file_path: str) -> None:
        """Show the diff content of a file."""
        content = self.query_one("#main-content", RichLog)
        content.clear()

        # Update the title
        self.query_one(".section-title", Label).update(f"[bold]4-Diff: {file_path}[/bold]")

        # Add some dummy diff content
        content.write("[green]diff --git a/app.py b/app.py[/green]")
        content.write("[green]index 1234567..abcdefg 100644[/green]")
        content.write("[green]--- a/app.py[/green]")
        content.write("[green]+++ b/app.py[/green]")
        content.write("[cyan]@@ -20,7 +20,7 @@[/cyan] def some_function():")
        content.write("     # Some comment")
        content.write("     print('Hello')")
        content.write("[red]-    return False[/red]")
        content.write("[green]+    return True[/green]")
        content.write("     ")
        content.write("     # Another comment")
        content.write("[cyan]@@ -35,6 +35,9 @@[/cyan] def another_function():")
        content.write("     # Process data")
        content.write("[green]+    # New functionality[/green]")
        content.write("[green]+    result = process_data()[/green]")
        content.write("[green]+    return result[/green]")

    def show_commit_details(self, commit_hash: str) -> None:
        """Show the details of a commit."""
        content = self.query_one("#main-content", RichLog)
        content.clear()

        # Update the title
        self.query_one(".section-title", Label).update(f"[bold]4-Commit: {commit_hash}[/bold]")

        # Add commit details
        content.write(f"[yellow]commit[/yellow] [green]{commit_hash}[/green]")
        content.write("[blue]Author:[/blue] Ayush <mail@ayush.dev>")
        content.write("[blue]Date:[/blue]   3 minutes ago")
        content.write("")
        content.write("    widgets cn 1")
        content.write("    ")
        content.write("    [blue]Signed-off-by:[/blue] Ayush <mail@ayush.dev>")
        content.write("")
        content.write("[bold]Changed files:[/bold]")
        content.write("[red]- app.py[/red]")
        content.write("[red]- README.md[/red]")
        content.write("[green]+ utils.py[/green]")

    def show_welcome(self) -> None:
        """Show welcome message."""
        content = self.query_one("#main-content", RichLog)
        content.clear()

        # Update the title
        self.query_one(".section-title", Label).update("[bold]4-Welcome[/bold]")

        # Add welcome content
        content.write("[bold]Welcome to GitX - A beginner-friendly Git TUI[/bold]")
        content.write("")
        content.write("[green]•[/green] Select files to view and manage them")
        content.write("[green]•[/green] View commit history and branch information")
        content.write("[green]•[/green] Use keyboard shortcuts shown at the bottom")
        content.write("[green]•[/green] Run custom Git commands in the command panel")
        content.write("")
        content.write("Press [bold]?[/bold] for help and available commands")
