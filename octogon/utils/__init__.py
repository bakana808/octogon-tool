import os


class defaultdict(dict):
    def get_or_default(self, key, fn):
        """
        If the key exists in this dict, return the value,
        else call the function.
        """
        if key in self:
            return self[key]
        else:
            value = fn()
            self[key] = value
            return value


def list_file_basenames(path: str):
    """Get a list of files (no extension) in a folder."""
    _, _, filenames = next(os.walk(path))
    return [os.path.splitext(f)[0] for f in filenames]
