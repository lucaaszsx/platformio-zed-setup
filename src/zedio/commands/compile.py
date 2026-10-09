from pathlib import Path

from zedio.common import parser_env_parent
from zedio.lib import logger
from zedio.lib.pio import pio_compile
from zedio.lib.prompts import select_env


def register(subparsers):
    parser = subparsers.add_parser(
        "compile",
        parents=[parser_env_parent],
        help="compile the project",
        description="Compile the current PlatformIO project."
    )
    parser.set_defaults(run=run)

    return parser

def run(args):
    project_path = Path.cwd()
    env = args.env or select_env(cwd=project_path)

    logger.info(f"Compiling project: {project_path.name}")
    pio_compile(cwd=project_path, env=env)

    return 0
