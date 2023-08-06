import sys
from argparse import HelpFormatter
from functools import lru_cache, partial
from io import BytesIO
from subprocess import check_output, SubprocessError


def error(message):
    """Write an error to the console"""
    print(f'\033[31mError:\033[0m {message}', file=sys.stderr)
    return 1


def b2s(binary):
    """
    Binary to string helper which ignores all data which can't be decoded
    :param binary: Binary bytes string
    :return: String
    """
    return binary.decode(encoding='ascii', errors='ignore')


def b2s_file(binary_file):
    """
    File based binary to string helper
    :param binary_file: Binary file to convert
    :return: The same file object with a patched method
    """
    orig = binary_file.read
    binary_file.read = lambda *a, **k: b2s(orig(*a, **k))
    return binary_file


def log(message):
    print(message, file=sys.stderr)
    return 0


@lru_cache()
def wc(file):
    """Get number of lines in a file"""
    with open(file, mode='rb') as fd:
        return sum(1 for _ in fd)


def handle_interrupt(func):
    """Decorator which ensures that keyboard interrupts are handled properly."""
    def wrapper():
        try:
            return func() or 0
        except KeyboardInterrupt:
            print('\n\033[31mError:\033[0m Aborted.')
            return 1
    return wrapper


def print_diagnostic_info():
    """
    Get info about the current system used in bug reports
    Please fill out the damn bug reports people, how hard is it
    """
    from stegcracker import __version__

    def run(cmd):
        try:
            return f'$ {cmd}\n' + check_output(cmd, shell=True).decode()
        except SubprocessError:
            return 'unknown'

    err = partial(print, file=sys.stderr)

    err('### Command Used')
    err('```')
    err('$ ' + (' '.join(sys.argv)))
    err('```\n')

    err('### StegCracker Version')
    err('```')
    err(__version__)
    err('```\n')

    err('### StegCracker Type')
    err('```')
    err(run('file $(which stegcracker)'))
    err('```\n')

    err('### StegHide Version')
    err('```')
    err(run('steghide --version'))
    err('```\n')

    err('### Python Version')
    err('```')
    err(sys.version)
    err('```\n')

    err('### System Version')
    err('```')
    err(run('uname -a'))
    err(run('cat /etc/issue'))
    err('```\n')


class DevNull(BytesIO):
    def write(self, *_): pass

    def read(self, *_): return b''


class CustomHelpFormatter(HelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, indent_increment=2, max_help_position=7, width=None)

    # noinspection PyProtectedMember
    def _format_action(self, action):
        result = super(CustomHelpFormatter, self)._format_action(action) + "\n"

        if 'show this help message and exit' in result:
            result = result.replace('show', 'Show', 1)

        return result
