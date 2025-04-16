from textual.widgets import Static, Input, Button
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Label
from rich.text import Text


class CommandPanel(Static):
    """Panel for executing custom Git commands."""

    def compose(self) -> ComposeResult:
        """Compose the command panel."""
        yield Vertical(
            Label("[bold]5-Command log[/bold]", classes="section-title"),
            Horizontal(
                Input(placeholder="Enter git command...", id="command-input"),
                Button("Run", id="run-command-btn", variant="primary"),
                id="command-row"
            ),
            Static("You can hide/focus this panel by pressing '@'", id="command-output"),
            id="command-panel",
            classes="panel"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press event."""
        if event.button.id == "run-command-btn":
            command_input = self.query_one("#command-input", Input)
            command = command_input.value

            if command.strip():
                output = self.query_one("#command-output", Static)
                output_text = Text(f"$ git {command}\n")
                output_text.stylize("yellow")

                # Add dummy response
                response = Text("Executing command...\n")
                response.stylize("green")

                output.update(output_text + response)

                # Clear the input field after execution
                command_input.value = ""

                # Focus back on input for next command
                self.app.set_focus(command_input)

                # Notify user about command execution
                self.app.notify(f"Executed: git {command}")
            else:
                self.app.notify("Please enter a command", severity="warning")
