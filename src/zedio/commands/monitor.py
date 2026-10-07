from zedio.lib import logger
from zedio.lib.pio import pio_monitor
from zedio.lib.prompts import select_port


def register(subparsers):
    parser = subparsers.add_parser(
        "monitor",
        help="open the serial monitor",
        description="Open a serial monitor on the connected board."
    )
    parser.add_argument(
        "-p", "--port",
        metavar="<port>",
        help="port used for monitor"
    )
    parser.set_defaults(run=run)

    return parser

def run(args):
    port = args.port or select_port(message="Which port you want to monitor?", allow_none=True, ignore_only_none=True)
    if port is None:
        logger.warn("No active port found. PlatformIO will attempt to infer a port based on the connected devices")

    pio_monitor(port)

    return 0
