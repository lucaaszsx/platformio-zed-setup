from pathlib import Path

from InquirerPy.prompts.input import InputPrompt as text

from zedio.common import parser_env_parent
from zedio.lib import logger
from zedio.lib.pio import pio_upload
from zedio.lib.prompts import select_env, select_port

import shlex

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
    project_path = Path.cwd()
    env = args.env or select_env(cwd=project_path)
    use_monitor = args.use_monitor or args.monitor_port is not None
    same_port = args.same_port or args.same_port is not None
    port = None
    upload_port = None
    monitor_port = None

    if same_port:
        port = select_port(message="Select an port for upload/monitor:", allow_none=True)
    if not same_port:
        upload_port = select_port(message="Select an port for upload:", allow_none=True)

        if use_monitor:
            monitor_port = select_port(message="Select an port for monitor:", allow_none=True)
    if not port or not (upload_port or monitor_port):
        logger.info("No port was specified. PlatformIO will attempt to infer a port based on the connected devices")

    upload_cmd, upload_runnable = pio_upload(
        cwd=project_path,
        common_port=port,
        env=env,
        monitor_port=monitor_port,
        upload_port=upload_port,
        same_port=same_port,
        use_monitor=use_monitor
    )

    logger.info(f"Uploading project environment: {env}")
    logger.info(f"  {shlex.join(upload_cmd)}")
    upload_runnable.trigger()

    logger.success("Finish.")

    return 0
