from datetime import datetime
from time import sleep
from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextArea
from textual.containers import VerticalScroll


class Markdown(TextArea):
    def on_mount(self) -> TextArea:
        todays_date = self.get_date()

        self.markdown_path = Path.home() / "daily_log.md"
        if self.markdown_path.exists():
            text = open(self.markdown_path).read()
            if not todays_date in text:
                text += f"\n\n# {todays_date}"
            self.load_text(f"{text}\n")
            self.cursor_location = (text.count("\n"), 0)
            return
        self.load_text(f"# {todays_date}\n")
        self.cursor_location = (2, 0)

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
        # TODO incorporate markdown viewer into
        yield VerticalScroll(
            Markdown(language="markdown", id="text"),
        )

    def on_mount(self) -> None:
        self.flag = False
        self.markdown_path = Path.home() / "daily_log.md"

    # Actions connect to bindings with the action_* keyword
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit(self) -> None:
        t = self.query_one("#text").text
        with open(str(self.markdown_path), "w") as log:
            log.write(t)

        self.exit()


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
