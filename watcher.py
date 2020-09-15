import os
from scss.compiler import Compiler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


def scss_compile(path):
    """Compiles SCSS into CSS."""

    # don't compile non-scss files
    if os.path.splitext(path)[1] != ".scss":
        return

    try:
        output_path = os.path.splitext(path)[0] + ".css"
        print(f"compiling SCSS at {path}")
        with open(output_path, "w") as f:
            f.write(Compiler(search_path=("style/",)).compile(path))
    except Exception as e:
        print("failed to compile scss: ")
        print(e)


def scss_batch_compile(path):
    """Compiles all SCSS files in a folder."""

    print(f"compiling all SCSS files in {path}")

    try:
        files = [
            f
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ]
        files = [os.path.join(path, f) for f in files]

        for filepath in files:
            scss_compile(filepath)
    except Exception as e:
        print(e)


class SCSSParserEventHandler(FileSystemEventHandler):
    def on_modified(self, event: FileModifiedEvent):
        path = event.src_path
        if os.path.splitext(path)[1] == ".scss":
            scss_batch_compile(os.path.dirname(path))


def start_watcher():
    """Watch changes in SCSS files and compile them into CSS."""

    observer = Observer()
    event_handler = SCSSParserEventHandler()
    observer.schedule(event_handler, path="style/", recursive=True)

    scss_batch_compile("style/")

    return observer
