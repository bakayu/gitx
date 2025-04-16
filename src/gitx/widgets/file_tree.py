from textual.widgets import Tree, Static
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label


class FileTree(Static):
    """Tree view for displaying unstaged/untracked files."""

    def compose(self) -> ComposeResult:
        """Compose the file tree."""
        yield Vertical(
            Label("[bold]2-Files[/bold]", classes="section-title"),
            Tree("Files", id="file-tree"),
            classes="panel"
        )

    def on_mount(self) -> None:
        """Set up the tree when mounted."""
        self.refresh_tree()

    def refresh_tree(self) -> None:
        """Refresh the file tree with current repository status."""
        tree = self.query_one(Tree)
        tree.clear()

        try:
            # Get the actual status from git
            status = self.app.git.get_status()

            # Add sections for different file statuses
            if status.get("staged"):
                staged = tree.root.add("Staged Changes", expand=True)
                for file in status["staged"]:
                    node = staged.add_leaf(file)
                    node.data = {"status": "staged", "path": file}

            if status.get("modified"):
                unstaged = tree.root.add("Unstaged Changes", expand=True)
                for file in status["modified"]:
                    node = unstaged.add_leaf(file)
                    node.data = {"status": "modified", "path": file}

            if status.get("deleted"):
                deleted_node = tree.root.add("Deleted Files", expand=True)
                for file in status["deleted"]:
                    node = deleted_node.add_leaf(file)
                    node.data = {"status": "deleted", "path": file}

            if status.get("untracked"):
                untracked = tree.root.add("Untracked Files", expand=True)
                for file in status["untracked"]:
                    node = untracked.add_leaf(file)
                    node.data = {"status": "untracked", "path": file}

            # Add styling to tree nodes
            self.apply_tree_styling()
        except Exception as e:
            # If there's an error, add an error node
            error_node = tree.root.add("Error")
            error_node.add_leaf(f"Error: {str(e)}")

    def apply_tree_styling(self) -> None:
        """Apply appropriate CSS classes to tree nodes based on their status."""
        tree = self.query_one(Tree)

        # Walk all children and manually skip the root node
        for node in tree.walk_children():
            # Skip the root node
            if node is tree.root:
                continue

            if hasattr(node, 'data') and node.data:
                if node.data.get("status") == "modified":
                    node.label.stylize("red")
                elif node.data.get("status") == "untracked":
                    node.label.stylize("magenta")
                elif node.data.get("status") == "staged":
                    node.label.stylize("green")
                elif node.data.get("status") == "deleted":
                    node.label.stylize("red dim")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle tree node selection."""
        node = event.node

        # Only process file nodes (not category nodes)
        if hasattr(node, 'data') and node.data and "path" in node.data:
            file_path = node.data["path"]
            status = node.data["status"]

            # Show the diff in the main panel
            main_panel = self.app.query_one('MainPanel')
            is_staged = status == "staged"
            main_panel.show_file_diff(file_path, staged=is_staged)
