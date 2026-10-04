from zedio.common import parser_env_parent


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
    return 0