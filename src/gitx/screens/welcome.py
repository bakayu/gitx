"""Welcome screen for gitx."""

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Header, Footer, Static


class WelcomeScreen(Screen):
    """Welcome screen displayed when the application starts."""

    def compose(self) -> ComposeResult:
        """Compose the welcome screen layout."""
        yield Header(show_clock=True)
        yield Container(classes="welcome")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        welcome_container = self.query_one(".welcome", Container)
        welcome_container.mount(
            Static("gitx", classes="welcome-title"),
            Static("A Terminal User Interface for Git", classes="welcome-text"),
            Static("Press 't' to toggle theme or 'q' to quit", classes="welcome-text"),
        )
