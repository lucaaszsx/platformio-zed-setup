import argparse
import sys

from zedio.commands import compile, create_project, generate_commands, monitor, upload, setup
from zedio.lib import logger
from zedio.lib.errors import PioError


def main():
    parser = argparse.ArgumentParser(
        prog="zedio",
        description="PlatformIO project manager for Zed Editor",
        usage="zedio <command> [options]",
        epilog="Run 'zedio <command> --help' for details on a specific command."
    )
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        metavar="<command>",
        required=True
    )

    for command in (compile, create_project, generate_commands, monitor, upload, setup):
        command.register(subparsers)

    args = parser.parse_args()

    try:
        return args.run(args)
    except KeyboardInterrupt:
        logger.warn("Operation aborted")
        return 130
    except PioError as e:
        logger.error(str(e))
        return 1
    except OSError as e:
        logger.error(f"Something went wrong: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
