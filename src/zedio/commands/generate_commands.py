from zedio.common import parser_env_parent


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
    return 0