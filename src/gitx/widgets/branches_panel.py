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
        self.refresh_branches()

    def refresh_branches(self) -> None:
        """Refresh the branches tree with current repository branches."""
        tree = self.query_one(Tree)
        tree.clear()

        try:
            # Get actual branches from git
            branches = self.app.git.get_branches()
            current_branch = self.app.git.get_current_branch()

            if not branches:
                tree.root.add_leaf("No branches found")
                return

            # Add branches to tree with proper styling
            for branch_info in branches:
                branch = branch_info["name"]
                node = tree.root.add_leaf(branch)
                node.data = {"branch": branch}

                if branch == current_branch:
                    # Current branch in green with check mark
                    node.label.stylize("green bold")
                    node.label = Text("✓ ") + node.label


            # Get remote branches
            remote_branches = []
            for branch_info in branches:
                if branch_info.get("remote"):
                    remote_branches.append(branch_info["remote"])

            # Add any remote branches that don't have a local counterpart
            if remote_branches:
                for remote_branch in remote_branches:
                    if "/" in remote_branch:  # Make sure it's a valid remote branch
                        node = tree.root.add_leaf(remote_branch)
                        node.data = {"branch": remote_branch}
                        node.label.stylize("blue")

            # Expand the tree by default
            tree.root.expand()
        except Exception as e:
            tree.root.add_leaf(f"Error: {str(e)}")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle tree node selection."""
        node = event.node

        if hasattr(node, 'data') and node.data and "branch" in node.data:
            branch = node.data["branch"]

            # Show dialog to confirm checkout or perform related branch action
            self.app.notify(f"Selected branch: {branch} (checkout not implemented yet)")
