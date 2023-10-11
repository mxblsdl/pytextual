from datetime import datetime
from time import sleep
from pathlib import Path

from textual import events
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Header, Footer, Static, TextArea, Button, Label
from textual.containers import Grid, ScrollableContainer, Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.events import Key



class Markdown(TextArea):
    def on_mount(self) -> TextArea:
        self.load_text(f"# {self.get_date()}\n")
        self.cursor_location = (2, 0)
        print(self.text)

    def get_date(self) -> str:
        return datetime.today().strftime("%m/%d/%Y")

    def check_for_dash(self) -> bool:
        row = self.cursor_location[0]
        line = self.get_text_range((row, 0), (row, 300))  # arbitrarily large number
        text = line.strip()
        return text.startswith("-")

    def _on_key(self, event: events.Key) -> None:
        if event.character == "(":
            self.insert("()")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()

        if event.key == "enter" and self.check_for_dash():
            # self.document.newline
            self.insert("\n- ")
            event.prevent_default()


class MarkdownApp(App):
    """The main application extends the app class"""

    def on_key(self, event: Key):
        if self.flag == True:
            self.query_one("#startup").remove()
            self.flag = not self.flag

    CSS_PATH = "./styles/styles.tcss"
    TITLE = "Markdown Editor"
    BINDINGS = [
        ("ctrl+d", "toggle_dark", "Toggle Dark Mode"),
        ("ctrl+c", "quit", "Quit the app"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header(show_clock=True, name="Stopwatch!")
        yield Footer()
        # TODO save file on exit
        # TODO read from file and load into text
        # TODO behaviour for no press
        # TODO incorporate markdown viewer into
        yield VerticalScroll(
            ScrollableContainer(
                Static(
                    "No Daily log file found. Do you want to create one?", id="message"
                ),
                Button.success(label="Yes", id="yes"),
                Button.warning(label="No", id="no"),
                id="startup",
            ),
            Markdown(language="markdown", id="text"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Do an action depending on which button was pressed
        id = event.button.id
        if id == "yes":
            home_path = Path.home() / "daily_log.md"
            home_path.touch()  #! comment out for testing
            self.query_one("#startup").mount(
                Label(
                    f"Daily log file created at {str(home_path)}\nPress any key to continue"
                ),
                before=0,
            )
            self.query_one("#message").remove()
            self.flag = True

    def on_mount(self) -> None:
        self.flag = False
        self.markdown_path = Path.home() / "daily_log.md"
        if self.markdown_path.exists():
            self.query("#startup").remove()

    # Actions connect to bindings with the action_* keyword
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit(self) -> None:
        t = self.query_one("#text").text
        self.exit(message=t)


def run() -> None:
    """Run the application
    There is a good example here:
    https://github.com/Textualize/frogmouth/blob/main/frogmouth/app/app.py
    Which should be used for passing in arguments to the run command
    """
    MarkdownApp().run()


if __name__ == "__main__":
    MarkdownApp().run()


# textual run --dev app.py
