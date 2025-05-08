from colorama import Fore, Style, init


def green(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def red(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def cyan(text):
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"


def bold(text):
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"

def white(text):
    return f"{Fore.RESET}{text}{Style.RESET_ALL}"

def highlight(value, ceil, floor):
    if value >= ceil:
        return green(value)
    elif value <= floor:
        return red(value)
    else:
        return white(value)