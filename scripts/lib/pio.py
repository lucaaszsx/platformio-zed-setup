import json
import subprocess
import sys
from pathlib import Path

from lib.common import PROJECTS_FOLDER, Colors, print_format


def find_project(directory: str) -> Path:
    root = Path(PROJECTS_FOLDER)
    start = Path(directory).resolve()

    if root not in start.parents:
        print_format(Colors.FAIL, f"\"{start}\" is not inside \"{root}\"")
        sys.exit(1)

    for path in (start, *start.parents):
        if path == root:
            break
        if (path / "platformio.ini").is_file():
            return path

    print_format(Colors.FAIL, f"platformio.ini not found between {start} and {root}")
    sys.exit(1)

def pio_call(project: Path, args: list[str]):
    return subprocess.call(["pio", *args], cwd=project)

def pio_output(args: list[str], project: Path | None = None) -> str:
    if project:
        return subprocess.run(["pio", *args], cwd=project, stdout=subprocess.PIPE, text=True, check=True).stdout
    else:
        return subprocess.run(["pio", *args], stdout=subprocess.PIPE, text=True, check=True).stdout

def pio_load_conf(project: Path):
    try:
        conf = json.loads(pio_output(["project", "config", "--json-output"], project))
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print_format(Colors.FAIL, f"Could not load project configuration from {project.name}: {e}")
        sys.exit(1)

    return conf

def pio_load_boards():
    try:
        boards = json.loads(pio_output(["boards", "--json-output"]))
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print_format(Colors.FAIL, f"Could not load boards: {e}")
        sys.exit(1)

    return boards
