def register(subparsers):
    parser = subparsers.add_parser(
        "monitor",
        help="open the serial monitor",
        description="Open a serial monitor on the connected board."
    )
    parser.set_defaults(run=run)

    return parser

def run():
    return 0
