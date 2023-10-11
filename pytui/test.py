import textual

def handle_key_event(event: textual.events.key):
    if event.key == textual.keys.shift:
        print("Shift key pressed!")

def main():
    app = textual.App()

    # Add a listener for key events.
    app.add_listener(textual.KeyType.KEY_PRESS, handle_key_event)

    # Start the app.
    app.run()

if __name__ == "__main__":
    main()
