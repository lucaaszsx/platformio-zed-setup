import os
import re
import shlex
from pathlib import Path

from InquirerPy.base.control import Choice
from InquirerPy.prompts.confirm import ConfirmPrompt as confirm
from InquirerPy.prompts.fuzzy import FuzzyPrompt as fuzzy
from InquirerPy.prompts.input import InputPrompt as text

from zedio.lib import logger
from zedio.lib.pio import pio_compiledb, pio_load_boards, pio_project_init
from zedio.lib.prompts import select_env
from zedio.templates.template_map import (
    TEMPLATE_MAP,
    template_dest_path,
    template_src_path,
)


def register(subparsers):
    parser = subparsers.add_parser(
        "init",
        help="initialize a PlatformIO project configured for Zed",
        description="Create a new PlatformIO project and generate the Zed configuration files."
    )
    parser.add_argument(
        "-n", "--name",
        help="name of the project",
        metavar="<name>"
    )
    parser.add_argument(
        "-b", "--board",
        help="board identifier (e.g. uno, esp32dev)",
        metavar="<board>"
    )
    parser.add_argument(
        "-f", "--framework",
        help="framework to use (e.g. arduino, espidf)",
        metavar="<framework>"
    )
    parser.add_argument(
        "-s", "--monitor-speed",
        metavar="<baud>",
        help="serial monitor speed (default: 115200)"
    )
    parser.add_argument(
        "--sample-code",
        action="store_true",
        default=None,
        help="generate a sample source file"
    )
    parser.add_argument(
        "--compiledb",
        action="store_true",
        default=None,
        help="generate a sample source file"
    )
    parser.set_defaults(run=run)

    return parser

def run(args):
    project_name = args.name or text(message="What will be the name of the project?").execute()

    if not project_name:
        proceed = confirm(message="Project will be created on the current folder, since no name was specified, confirm?", default=True).execute()
        if not proceed:
            logger.info("Aborted")
            return 0
    elif not re.fullmatch(r"[A-Za-z0-9_-]+$", project_name):
        logger.error("Project name must contain characters from A-Z (lower and upper case), 0-9, underscores and hyphens")
        return 1

    project_path = (Path.cwd() / (project_name or ".")).resolve()
    project_name = project_path.name

    if project_path.exists() and project_path.is_file():
        logger.error(f"'{project_name}' exists and its a file")
        return 1

    if project_path.exists() and any(project_path.iterdir()):
        if project_path == Path.cwd():
            logger.error("The current directory is not empty")
        else:
            logger.error(f"Directory '{project_name}' already exists and is not empty")
        return 1

    logger.info("Loading boards")

    board_arg = args.board
    boards = pio_load_boards(board_arg) if board_arg else pio_load_boards()

    if not boards:
        logger.error(f"No boards found for: {board_arg}" if board_arg else "Couldn't load boards")
        return 1

    board = next((b for b in boards if b["id"] == board_arg), None)

    if not board:
        if board_arg:
            logger.warn(f"Board not found: {board_arg}. Select one from the matches below")

        board = fuzzy(
            message="Board:",
            choices=[Choice(value=b, name=f"{b["name"]} ({b["id"]})") for b in boards],
            default=board_arg or ""
        ).execute()

    logger.info(f"Using board: {board["name"]} ({board["id"]})")

    framework_arg = args.framework
    framework = next((f for f in board["frameworks"] if f == framework_arg), None)

    if not framework:
        if framework_arg:
            logger.warn(f"Framework '{framework_arg}' not found for board '{board["name"]}'")

        framework = fuzzy(
            message="Which framework will be used?",
            choices=board["frameworks"],
            default=framework_arg or ""
        ).execute()

    monitor_speed = args.monitor_speed or text("What will be the monitor speed (baud)?", default="115200").execute()

    if not isinstance(monitor_speed, str) or not monitor_speed.isdigit():
        logger.error("Monitor speed must be a number")
        return 1

    sample_code = args.sample_code or confirm(message="Do you want to generate sample code?", default=True).execute()
    run_compiledb = args.compiledb or confirm(message="Do you want to generate compile commands after creating the project?", default=True).execute()

    try:
        logger.info("Creating the project")
        os.makedirs(project_path, exist_ok=True)

        init_cmd, runnable = pio_project_init(
            cwd=project_path,
            board=board["id"],
            framework=framework,
            monitor_speed=monitor_speed,
            sample_code=sample_code
        )

        logger.info("Initializing project with PlatformIO")
        logger.info(f"  {shlex.join(init_cmd)}")
        runnable.trigger()

        logger.info(f"Copying template files to \"{project_name}\"")

        for key in TEMPLATE_MAP:
            src = template_src_path(key)
            dest = template_dest_path(key, project_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

            logger.info(f"  Created {dest.relative_to(project_path)}")

        logger.success("Project successfully created")

        if not run_compiledb:
            return 0

        env = select_env(cwd=project_path, message="Which environment for compile commands generation?")

        logger.info("Generating compile commands for LSP")
        pio_compiledb(cwd=project_path, env=env)
    except KeyboardInterrupt:
        logger.warn("Operation aborted")
        return 130
    except OSError as e:
        logger.error(f"Something went wrong: {e}")
        return 1

    return 0
