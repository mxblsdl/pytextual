from datetime import datetime
from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextArea, Markdown
from textual.containers import VerticalScroll


class MyTextArea(TextArea):
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

        if event.character == "[":
            self.insert("[]")
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
        # ("ctrl+d", "delete_line", "Delete Line"),
        ("ctrl+c", "quit", "Quit the app"),
        ("ctrl+n", "markdown", "Markdown View"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header(show_clock=True, name="Stopwatch!")
        yield Footer()
        yield VerticalScroll(
            MyTextArea(language="markdown", id="text"),
            Markdown(id="viewer"),
            id="editor",
        )

    def on_mount(self) -> None:
        self.query_one("#viewer").styles.height = "0"

        self.flag = False
        self.viewer = False
        self.markdown_path = Path.home() / "daily_log.md"
        self.set_focus(self.query_one("#text"))

    def action_markdown(self) -> None:
        if self.viewer:
            text = "100%"
            viewer = "0"
        else:
            text = "0"
            viewer = "100%"
        self.viewer = not self.viewer

        text_comp = self.query_one("#text")
        text_comp.styles.height = text

        viewer_comp = self.query_one("#viewer")
        viewer_comp.styles.height = viewer
        viewer_comp.update(text_comp.text)

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
