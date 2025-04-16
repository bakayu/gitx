from textual.widgets import Static, Tree
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label
from rich.text import Text


class BranchesPanel(Static):
    """Panel that displays and manages branches."""

    def compose(self) -> ComposeResult:
        """Compose the branches panel."""
        yield Vertical(
            Label("[bold]3-Local branches[/bold]", classes="section-title"),
            Tree("Branches", id="branches-tree"),
            classes="panel"
        )

    def on_mount(self) -> None:
        """Set up the tree when mounted."""
        tree = self.query_one(Tree)

        # Add local branches
        current_branch = "feat/init-git-commands"
        branches = [
            "master",
            "feat/init-git-commands",
            "feat/init-gitx-app",
            "doc/tutorial-update",
            "feat/lint-ci",
            "origin/feat/lint-ci",
            "feat/ghactions-docs",
            "feat/mkdocs-integrate"
        ]

        # Add branches to tree with proper styling
        for branch in branches:
            node = tree.root.add_leaf(branch)
            if branch == current_branch:
                # Current branch in green with check mark
                node.label.stylize("green bold")
                node.label = Text("✓ ") + node.label
            elif branch.startswith("origin/"):
                # Remote branches in blue
                node.label.stylize("blue")

        # Expand the tree by default
        tree.root.expand()
