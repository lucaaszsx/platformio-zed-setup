import os
import sys

_LEVELS = {
    "info": ("info", "\033[34m"),
    "warn": ("warn", "\033[33m"),
    "error": ("error", "\033[31m"),
    "success": ("ok", "\033[32m"),
}
_RESET = "\033[0m"


def _log(level, message, stream):
    label, color = _LEVELS[level]
    tag = f"[{label}]"

    if stream.isatty() and "NO_COLOR" not in os.environ:
        tag = f"{color}{tag}{_RESET}"
    print(f"{tag} {message}", file=stream)

def info(message):
    _log("info", message, sys.stdout)


def success(message):
    _log("success", message, sys.stdout)


def warn(message):
    _log("warn", message, sys.stderr)


def error(message):
    _log("error", message, sys.stderr)
