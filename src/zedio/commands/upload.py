from zedio.common import parser_env_parent


def register(subparsers):
    parser = subparsers.add_parser(
        "upload",
        parents=[parser_env_parent],
        help="upload the firmware to the board",
        description="Build the project and upload the firmware to the connected board."
    )
    parser.add_argument(
        "-m", "--use-monitor",
        action="store_true",
        help="open the serial monitor after uploading"
    )
    parser.add_argument(
        "--same-port",
        action="store_true",
        help="use the same port for upload and monitor"
    )
    parser.add_argument(
        "-p", "--port",
        metavar="<port>",
        help="port used for both upload and monitor (requires --same-port)"
    )
    parser.add_argument(
        "--upload-port",
        metavar="<port>",
        help="port used for upload"
    )
    parser.add_argument(
        "--monitor-port",
        metavar="<port>",
        help="port used for the serial monitor (requires --use-monitor)"
    )
    parser.set_defaults(run=run)

    return parser

def run(args):
    return 0