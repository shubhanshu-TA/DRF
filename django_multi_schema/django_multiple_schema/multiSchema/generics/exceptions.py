class MissingRequestParamsError(Exception):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return (
            "{0}:{1} is invalid input, Request can only accept valid "
            "values".format(self.key, self.value)
        )


class NoDataError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Data not available for the parameters received {0}".format(self.value)


class EmptyObjectError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
