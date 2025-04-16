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
        log = self.query_one(RichLog)

        # Make sure we start with an empty log
        log.clear()

        # Add dummy data that mimics LazyGit commit log styling
        log.write("[green]✱[/green] [yellow]commit[/yellow] [green]a215ea6[/green] ([red]HEAD → feat/init-git-commands[/red], [red]feat/init-widgets[/red])")
        log.write("│ [blue]Author:[/blue] Ayush <mail@ayush.dev>")
        log.write("│ [blue]Date:[/blue]   3 minutes ago")
        log.write("│ ")
        log.write("│     widgets cn 1")
        log.write("│ ")
        log.write("│     [blue]Signed-off-by:[/blue] Ayush <mail@ayush.dev>")
        log.write("│")
        log.write("[green]✱[/green] [yellow]commit[/yellow] [green]71d3e14[/green] ([red]origin/master[/red], [red]origin/HEAD[/red], [red]master[/red])")
        log.write("│\\ [blue]Merge:[/blue] 35d7366 6b16804")
        log.write("│ │ [blue]Author:[/blue] Anmol <anmolarora001@gmail.com>")
        log.write("│ │ [blue]Date:[/blue]   4 days ago")
        log.write("│ │ ")
        log.write("│ │     Merge pull request #12 from gitxtui/feat/init-gitx-app")
        log.write("│ │ ")
        log.write("│ │     feat+doc: init base app, change doc site styling")
        log.write("│ │")

        # Add more commits to simulate a longer history
        self._add_more_sample_commits(log)

    def _add_more_sample_commits(self, log):
        """Add more sample commits to fill the log."""
        log.write("[green]✱[/green] [yellow]commit[/yellow] [green]6b16804[/green] ([red]origin/feat/init-gitx-app[/red], [red]feat/init-gitx-app[/red])")
        log.write("│ [blue]Author:[/blue] Ayush <mail@ayush.dev>")
        log.write("│ [blue]Date:[/blue]   4 days ago")
        log.write("│ ")
        log.write("│     feat+doc: init base app, change doc site styling")
        log.write("│ ")
        log.write("│     [blue]Signed-off-by:[/blue] Ayush <mail@ayush.dev>")
        log.write("│")
        log.write("[green]✱[/green] [yellow]commit[/yellow] [green]35d7366[/green]")
        log.write("│\\ [blue]Merge:[/blue] 5796a72 86f8adc")
        log.write("│ │ [blue]Author:[/blue] Ashmit9955 <ashmit9955@gmail.com>")
        log.write("│ │ [blue]Date:[/blue]   7 days ago")
        log.write("│ │ ")
        log.write("│ │     Merge pull request #10 from gitxtui/doc/tutorial-update")
        log.write("│ │ ")
        log.write("│ │     Doc/tutorial update")

    def update_log(self, commits):
        """Update the commit log with real commit data."""
        log = self.query_one(RichLog)
        log.clear()

        # This would be implemented to display actual commit data
        # For now we'll just display the dummy data
        self.on_mount()
