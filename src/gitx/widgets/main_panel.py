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

    def show_file_diff(self, file_path: str, staged: bool = False) -> None:
        """Show the diff content of a file.

        Args:
            file_path: Path to the file
            staged: Whether to show the staged diff
        """
        content = self.query_one("#main-content", RichLog)
        content.clear()

        # Update the title
        staging_status = "Staged" if staged else "Unstaged"
        self.query_one(".section-title", Label).update(f"[bold]4-Diff: {file_path} ({staging_status})[/bold]")

        try:
            # Get the actual diff from git
            diff_output = self.app.git.get_file_diff(file_path, staged)

            if not diff_output:
                content.write("[yellow]No changes detected in this file.[/yellow]")
                return

            # Parse and colorize the diff output
            for line in diff_output.splitlines():
                if line.startswith("+") and not line.startswith("+++"):
                    content.write(f"[green]{line}[/green]")
                elif line.startswith("-") and not line.startswith("---"):
                    content.write(f"[red]{line}[/red]")
                elif line.startswith("@@"):
                    content.write(f"[cyan]{line}[/cyan]")
                elif line.startswith("diff") or line.startswith("index") or line.startswith("---") or line.startswith("+++"):
                    content.write(f"[green]{line}[/green]")
                else:
                    content.write(line)
        except Exception as e:
            content.write(f"[red]Error displaying diff: {str(e)}[/red]")

    def show_commit_details(self, commit_hash: str) -> None:
        """Show the details of a commit.

        Args:
            commit_hash: The commit hash to display
        """
        content = self.query_one("#main-content", RichLog)
        content.clear()

        # Update the title
        self.query_one(".section-title", Label).update(f"[bold]4-Commit: {commit_hash}[/bold]")

        try:
            # Get the actual commit details from git
            details = self.app.git.get_commit_details(commit_hash)

            if not details:
                content.write(f"[red]Could not find commit: {commit_hash}[/red]")
                return

            # Show basic commit info
            content.write(f"[yellow]commit[/yellow] [green]{details['hash']}[/green]")
            content.write(f"[blue]Author:[/blue] {details['author']}")
            content.write(f"[blue]Date:[/blue]   {details['date']}")
            content.write("")

            # Show commit message with proper indentation
            for line in details['message'].split("\n"):
                content.write(f"    {line}")
            content.write("")

            # Show changed files
            content.write("[bold]Changed files:[/bold]")

            for file in details['changed_files'].get('deleted', []):
                content.write(f"[red]- {file}[/red]")

            for file in details['changed_files'].get('modified', []):
                content.write(f"[yellow]~ {file}[/yellow]")

            for file in details['changed_files'].get('added', []):
                content.write(f"[green]+ {file}[/green]")
        except Exception as e:
            content.write(f"[red]Error displaying commit details: {str(e)}[/red]")

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
