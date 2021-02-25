class NestedDict:
    """
    A dictionary containing improved getter and setter functions
    to easily access deeply nested keys.
    """

    def __init__(self, dictionary: dict, is_writable=False):

        self.dictionary = dictionary

        # if False, deny editing to this dictionary
        self.is_writable = is_writable

    def __getitem__(self, k: str):
        """
        Get a value from the json object.

        The key is formatted as a period-separated list of keys.
        For example:

            data["a.b.c"]

        is equivalent to:

            data["a"]["b"]["c"]

        If the value is an instance of dict, then another instance of
        NestedDict is returned.
        """

        keys = k.split(".")
        value = self.dictionary
        for key in keys:
            value = value[key]

        return self._convert_value(value)

    def _convert_value(self, value):
        if isinstance(value, dict):
            return NestedDict(value, self.is_writable)
        elif isinstance(value, list):
            return [self._convert_value(i) for i in value]
        else:
            return value

    def on_data_changed(self, k, v):
        """Called when a value has changed."""
        pass

    def __setitem__(self, k, v):
        """Set a value in the json object"""

        if not self.is_writable:
            raise RuntimeError("cannot modify this dict, it is non-writable")

        keys = k.split(".")
        ret = self.dictionary
        for i, key in enumerate(keys):
            if i == len(keys) - 1:  # last elm
                ret[key] = v
            else:
                # silently make a new dict if it doesn't exist
                if key not in ret:
                    ret[key] = {}
                ret = ret[key]

        self.on_data_changed(k, v)
