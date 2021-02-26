import os
from pathlib import Path

from scss.compiler import Compiler
from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from octogon.utils.logger import get_print_fn

print = get_print_fn("scss")


class SCSSAutoCompiler(FileSystemEventHandler):
    """Handles the automatic compilation of .scss files."""

    # output directory of the compiled .css files
    OUTPUT_DIR = "site/style"

    def __init__(self, octogon):

        config = octogon.config

        self.octogon = octogon
        self.observer = Observer()
        self.observer.schedule(self, path=config.STYLE_PATH, recursive=True)
        self.batch_compile(config.STYLE_PATH)

    def start(self) -> Observer:
        self.observer.setDaemon(True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def on_modified(self, event: FileModifiedEvent):
        path = event.src_path
        if os.path.splitext(path)[1] == ".scss":
            self.batch_compile(os.path.dirname(path))

    def compile_file(self, path: str):
        """Compiles SCSS into CSS."""

        # don't compile non-scss files
        if os.path.splitext(path)[1] != ".scss":
            return

        # the name of the compiled file without extensions
        name = Path(path).stem
        output_path = os.path.join(SCSSAutoCompiler.OUTPUT_DIR, name + ".css")

        try:
            # ensure these folders exist
            os.makedirs(os.path.dirname(output_path))
        except FileExistsError:
            pass

        try:
            print(f"compiling SCSS at {path} => {output_path}")
            with open(output_path, "w") as f:
                f.write(Compiler(search_path=("style/",)).compile(path))
            self.octogon.on_compile(name, "scss", output_path)
        except Exception as e:
            print("failed to compile scss: ")
            print(e)

    def batch_compile(self, dirpath):
        """Compiles all SCSS files in a folder."""

        print(f"compiling all SCSS files in {dirpath}")

        try:
            files = [
                os.path.join(dirpath, f)
                for f in os.listdir(dirpath)
                if os.path.isfile(os.path.join(dirpath, f))
            ]

            for filepath in files:
                self.compile_file(filepath)
        except Exception as e:
            print(e)
