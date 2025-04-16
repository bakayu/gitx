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
        tree = self.query_one(Tree)

        # Add sections for different file statuses with LazyGit-like styling
        unstaged = tree.root.add("Unstaged Changes", expand=True)
        # Add files to the unstaged section
        for file in ["app.py", "README.md"]:
            node = unstaged.add_leaf(file)
            node.data = {"status": "modified"}

        untracked = tree.root.add("Untracked Files", expand=True)
        # Add files to the untracked section
        for file in ["file1.txt", "file2.py"]:
            node = untracked.add_leaf(file)
            node.data = {"status": "untracked"}

        staged = tree.root.add("Staged Changes", expand=True)
        # Add files to the staged section
        node = staged.add_leaf("utils.py")
        node.data = {"status": "staged"}

        # Add styling to tree nodes
        self.apply_tree_styling()

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
