import os
from scss.compiler import Compiler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import octogon.config

print = octogon.config.get_print_fn("scss")


class SCSSAutoCompiler(FileSystemEventHandler):
    def __init__(self):
        config = octogon.config.config
        self.observer = Observer()
        self.observer.schedule(self, path=config.STYLE_PATH, recursive=True)
        SCSSAutoCompiler.batch_compile(config.STYLE_PATH)

    def start(self) -> Observer:
        self.observer.setDaemon(True)
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def on_modified(self, event: FileModifiedEvent):
        path = event.src_path
        if os.path.splitext(path)[1] == ".scss":
            SCSSAutoCompiler.batch_compile(os.path.dirname(path))

    @staticmethod
    def compile_file(path):
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

    @staticmethod
    def batch_compile(dirpath):
        """Compiles all SCSS files in a folder."""

        print(f"compiling all SCSS files in {dirpath}")

        try:
            files = [
                os.path.join(dirpath, f)
                for f in os.listdir(dirpath)
                if os.path.isfile(os.path.join(dirpath, f))
            ]

            for filepath in files:
                SCSSAutoCompiler.compile_file(filepath)
        except Exception as e:
            print(e)
