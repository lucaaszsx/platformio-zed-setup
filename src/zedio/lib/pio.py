import json
import subprocess
from pathlib import Path

from zedio.lib.errors import PioError, PioProjectNotFoundError
from zedio.templates.template_map import template_dest_path


# Utility
class PioRunnable:
    def __init__(
        self,
        args: list[str],
        cwd: Path | None = None,
        capture_output: bool = False,
        text: bool = False
    ):
        self.args = args
        self.cwd = cwd
        self.capture_output = capture_output
        self.text = text

    def trigger(self):
        return pio_run(self.args, cwd=self.cwd, capture_output=self.capture_output, text=self.text)

def pio_run(
    args: list[str],
    cwd: Path | None = None,
    capture_output: bool = False,
    text: bool = False
):
    cmd = ["pio", *args]

    try:
        return subprocess.run(cmd, cwd=cwd, check=True, capture_output=capture_output, text=text)
    except FileNotFoundError as e:
        raise PioError("pio not found, run setup.sh") from e
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or "").strip()
        raise PioError(
            f"'{' '.join(cmd)}' failed with exit code {e.returncode}"
            + (f": {stderr}" if stderr else "")
        ) from e

def pio_output(args: list[str], cwd: Path | None = None) -> str:
    result = pio_run(args, cwd=cwd, capture_output=True, text=True)
    return result.stdout

def pio_json(args: list[str], cwd: Path | None = None):
    args = [*args, "--json-output"]

    try:
        return json.loads(pio_output(args, cwd))
    except json.JSONDecodeError as e:
        raise PioError(
            f"Failed to parse json output '{" ".join(["pio", *args])}': "
            f"{e.msg} (line {e.lineno}, column {e.colno})"
        ) from e

def pio_load_ini(cwd: Path):
    if not is_pio_project(cwd):
        raise PioProjectNotFoundError(cwd)

    return pio_json(["project", "config"], cwd)

def pio_load_envs(cwd: Path):
    if not is_pio_project(cwd):
        raise PioProjectNotFoundError(cwd)

    return [name.removeprefix("env:") for name, _ in pio_load_ini(cwd) if name.startswith("env:")]

def pio_load_boards(query: str | None = None):
    args = ["boards"]
    if query:
        args += [query]
    return pio_json(args)

def is_pio_project(cwd: Path):
    return (cwd / "platformio.ini").exists()

# Project-related methods
def pio_project_init(
    cwd: Path,
    board: str,
    monitor_speed: str,
    framework: str | None = None,
    sample_code: bool = True
):
    args = [
        "project", "init",
        "--board", board,
        "--project-option", f"monitor_speed={monitor_speed}",
        "--project-option", f"extra_scripts=pre:{template_dest_path("compiledbtc", cwd)}"
    ]

    if framework:
        args += ["--project-option", f"framework={framework}"]
    if sample_code:
        args += ["--sample-code"]

    return (args, PioRunnable(args, cwd=cwd))

def pio_compile(cwd: Path, env: str | None = None):
    if not is_pio_project(cwd):
        raise PioProjectNotFoundError(cwd)

    args = ["run"]
    if env:
        args += ["-e", env]

    return pio_run(args, cwd=cwd)

def pio_compiledb(cwd: Path, env: str | None = None):
    if not is_pio_project(cwd):
        raise PioProjectNotFoundError(cwd)

    args = ["run", "-t", "compiledb"]
    if env:
        args += ["-e", env]

    return pio_run(args, cwd=cwd)

def pio_upload(
    cwd: Path,
    env: str | None = None,
    use_monitor: bool = False,
    same_port: bool = True,
    common_port: str | None = None,
    upload_port: str | None = None,
    monitor_port: str | None = None
):
    if not is_pio_project(cwd):
        raise PioProjectNotFoundError(cwd)

    args = ["run", "-t", "upload"]

    if env:
        args += ["-e", env]
    if use_monitor:
        args += ["-t", "monitor"]

    if same_port and common_port:
        args += ["-p", common_port]
    elif not same_port:
        if upload_port:
            args += ["--upload-port", upload_port]
        if monitor_port:
            args += ["--monitor-port", monitor_port]

    return (args, PioRunnable(args, cwd=cwd))
