import argparse
import sys

from zedio.commands import compile, create_project, generate_commands, monitor, upload


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

    for command in (compile, create_project, generate_commands, monitor, upload):
        command.register(subparsers)

    args = parser.parse_args()
    return args.run(args)

if __name__ == "__main__":
    sys.exit(main())
