# Initialize output before importing any module, that can use colorama.
from ..system import init_output

init_output()

import os  # noqa: E402
import sys  # noqa: E402
from .. import logs  # noqa: E402
from ..argument_parser import Parser  # noqa: E402
from ..utils import get_installation_info  # noqa: E402
from .alias import print_alias  # noqa: E402
from .fix_command import fix_command  # noqa: E402
from .shell_logger import shell_logger  # noqa: E402


def main():
    parser = Parser()
    known_args = parser.parse(sys.argv)

    if known_args.help:
        parser.print_help()
    elif known_args.version:
        logs.version(get_installation_info().version,
                     sys.version.split()[0])
    elif known_args.command or 'TF_HISTORY' in os.environ:
        fix_command(known_args)
    elif known_args.alias:
        print_alias(known_args)
    elif known_args.shell_logger:
        shell_logger(known_args.shell_logger)
    else:
        parser.print_usage()
