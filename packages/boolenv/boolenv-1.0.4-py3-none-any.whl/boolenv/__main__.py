import os


TRUE_VALUES = (
    "1",
    "true",
    "t",
    "yes",
    "y",
)


def boolenv_validate(value):
    if str(value).lower() in TRUE_VALUES:
        return True
    return False


def boolenv(name):
    if not os.environ.get(name):
        return False
    return boolenv_validate(os.environ.get(name))
