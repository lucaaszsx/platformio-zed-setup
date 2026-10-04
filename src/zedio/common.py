import argparse

parser_env_parent = argparse.ArgumentParser(add_help=False)
parser_env_parent.add_argument(
    "-e", "--env",
    help="PlatformIO environment to use",
    metavar="<name>"
)
