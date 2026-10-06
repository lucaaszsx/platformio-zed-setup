from pathlib import Path

from InquirerPy.base.control import Choice
from InquirerPy.prompts.list import ListPrompt as select

from zedio.lib import pio
from zedio.lib.util import get_ports


def select_env(cwd: Path, message: str = "Which environment?"):
    envs = pio.pio_load_envs(cwd)
    choices = [*envs, Choice(value=None, name="No environment")]

    return select(
        message=message,
        choices=choices,
        default=envs[0] if envs else None,
    ).execute()


def select_port(message: str, allow_none: bool = False):
    choices = [
        Choice(value=port.device, name=f"{port.device} - {port.description}")
        for port in get_ports()
    ]
    if allow_none:
        choices.insert(0, Choice(value=None, name="None"))

    return select(message=message, choices=choices).execute()