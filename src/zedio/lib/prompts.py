from collections import deque
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

def select_port(message: str, allow_none = False):
    ports = get_ports()
    port_choices = deque([Choice(value=port.device, name=f"{port.device} - {port.description}")] for port in ports)
    if allow_none:
        port_choices.appendleft([Choice(value=None, name="None - PlatformIO try to infer")])

    return select(message=message, choices=list(port_choices), default=None)
