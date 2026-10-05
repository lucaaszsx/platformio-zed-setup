from pathlib import Path

from zedio.common import parser_env_parent
from zedio.lib import logger
from zedio.lib.pio import pio_compiledb
from zedio.lib.prompts import select_env


def register(subparsers):
    parser = subparsers.add_parser(
        "compiledb",
        parents=[parser_env_parent],
        help="generate compile_commands.json",
        description="Generate the compilation database (compile_commands.json) used by the language server."
    )
    parser.set_defaults(run=run)

    return parser

def run(args):
    project_path = Path.cwd()
    env = args.env or select_env(cwd=project_path)

    logger.info(f"Generating compile commands for project: {project_path.name}")
    pio_compiledb(cwd=project_path, env=env)

    return 0
