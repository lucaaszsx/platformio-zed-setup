import os
import sys
from pathlib import Path

import json5
from json5.dumper import ModelDumper
from json5.loader import ModelLoader

from zedio.lib import logger

TASK = {
    "label": "Zedio: create new project",
    "command": "zedio",
    "args": ["init"],
    "use_new_terminal": False,
    "allow_concurrent_runs": False,
    "reveal": "always"
}

def register(subparsers):
    parser = subparsers.add_parser(
        "setup",
        help="configure the global Zed task",
        description="Add task to the global Zed tasks.json"
    )
    parser.set_defaults(run=run)

    return parser

def run(_args):
    if sys.platform == "win32":
        config_dir = Path(os.environ["APPDATA"]) / "Zed"
    else:
        config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "zed"

    logger.info(f"Zed configuration directory: {config_dir}")

    tasks_path = config_dir / "tasks.json"
    config_dir.mkdir(parents=True, exist_ok=True)

    content = tasks_path.read_text(encoding="utf-8") if tasks_path.exists() else ""
    source = content if content.strip() else "[]"

    try:
        tasks = json5.loads(source)
    except json5.JSON5DecodeError as error:
        logger.error(f"Invalid {tasks_path}: {error}")
        return 1

    if any(task.get("label") == TASK["label"] for task in tasks):
        logger.info(f"Task \"{TASK['label']}\" already exists, nothing to do")
        return 0

    document = json5.loads(source, loader=ModelLoader())
    entry = json5.loads(json5.dumps(TASK, indent=4), loader=ModelLoader()).value
    entry.wsc_before = ["\n    "]
    document.value.values.append(entry)

    tasks_path.write_text(
        json5.dumps(document, dumper=ModelDumper()),  # type: ignore[arg-type]
        encoding="utf-8"
    )
    logger.info(f"Task \"{TASK['label']}\" added to {tasks_path}")

    return 0
