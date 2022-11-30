import inspect


def this_name():
    """Returns the name of the function that called this function"""
    return inspect.stack()[1].function
