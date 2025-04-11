from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Header, Footer, Static


class GitxApp(App):
    """A TUI Git client built with Textual."""

    CSS_PATH = "css/app.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit"),
        Binding(key="t", action="toggle_dark", description="Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the app layout using the welcome screen."""
        self.theme = "flexoki"  # Default theme
        yield Header(show_clock=True)
        yield Container(
            Static("Welcome to gitx!", classes="welcome-title"),
            Static("A Terminal User Interface for Git", classes="welcome-text"),
            Static("Press 't' to toggle theme or 'q' to quit", classes="welcome-text"),
            classes="welcome"
        )
        yield Footer()

    def action_toggle_dark(self) -> None:
        """Toggle between light and dark theme."""
        self.theme = (
            "flexoki" if self.theme == "catppuccin-latte" else "catppuccin-latte"
        )

def main() -> None:
    """Run the app."""
    app = GitxApp()
    app.run()


if __name__ == "__main__":
    main()
