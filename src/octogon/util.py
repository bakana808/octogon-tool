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
