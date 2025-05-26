__DEBUG = True


def debug_print(*args, **kwargs):
    """
    Print debug information if __DEBUG is True.
    """
    if __DEBUG:
        print("[Debug] ", end="")
        print(*args, **kwargs)


def print_error(*args, **kwargs):
    print("[Error] ", end="")
    print(*args, **kwargs)


def print_info(*args, **kwargs):
    print("[Info] ", end="")
    print(*args, **kwargs)
